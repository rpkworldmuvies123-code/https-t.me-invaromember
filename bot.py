import os
import csv
import io
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN environment variable.")

HELP_TEXT = (
    "Main kisi bhi public channel ke saare members ki list nahi nikal sakta. "
    "Telegram Bot API complete member lists expose nahi karta.\\n\\n"
    "Main public channel ki basic info check kar sakta hoon, aur jis channel "
    "mein bot ko permission ho wahan Telegram ke supported count method se "
    "member count dikhane ki koshish kar sakta hoon."
)

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔎 Check Channel", callback_data="check")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Telegram Channel Helper\\n\\n"
        "Channel ka @username check karne ke liye button dabao.\\n"
        "Note: bot saare channel members ke usernames export nahi kar sakta.",
        reply_markup=menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check":
        context.user_data["awaiting_channel"] = True
        await query.message.reply_text(
            "Channel ka public username bhejo, jaise @telegram. "
            "Sirf public channel ki basic information check hogi."
        )
    elif query.data == "help":
        await query.message.reply_text(HELP_TEXT, reply_markup=menu())

async def channel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_channel"):
        await update.message.reply_text("Shuru karne ke liye /start bhejo.")
        return

    raw = (update.message.text or "").strip()
    context.user_data["awaiting_channel"] = False

    if raw.startswith("https://t.me/"):
        raw = raw[len("https://t.me/"):].strip("/")
    if raw.startswith("@"):
        raw = raw[1:]
    if not raw or len(raw) > 64 or not all(c.isalnum() or c == "_" for c in raw):
        await update.message.reply_text("Username sahi nahi hai. Example: @telegram", reply_markup=menu())
        return

    try:
        chat = await context.bot.get_chat("@" + raw)
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or raw
        username = getattr(chat, "username", None)
        chat_id = chat.id
        count_text = "Member count: Telegram ne is bot ko count dene ki permission nahi di."
        try:
            count = await context.bot.get_chat_member_count(chat_id)
            count_text = f"Member count: {count:,}"
        except Exception:
            pass

        result = (
            "✅ Channel info mil gayi\\n\\n"
            f"Name: {title}\\n"
            f"Username: @{username if username else raw}\\n"
            f"Chat ID: {chat_id}\\n"
            f"{count_text}\\n\\n"
            "⚠️ Telegram Bot API kisi bhi channel ke saare members ke usernames "
            "nahi deta, isliye bulk member-list export available nahi hai."
        )
        await update.message.reply_text(result, reply_markup=menu())
    except Exception as exc:
        logger.info("Channel lookup failed: %s", type(exc).__name__)
        await update.message.reply_text(
            "Channel check nahi ho paya. Username verify karo aur confirm karo ki "
            "channel public hai. Kuch channels ki information bots ko available nahi hoti.",
            reply_markup=menu()
        )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Menu ke liye /start bhejo.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, channel_message))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    logger.info("Bot is starting")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
