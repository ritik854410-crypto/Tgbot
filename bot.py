from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.environ.get("8755042324:AAHGuUwodlbI2f2MwIAtt3SMk4jLAVnVQsA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💸 Daily Plan ₹10"],
        ["🔥 Weekly Plan ₹50"],
        ["👑 Monthly Plan ₹150"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome bhai!\n\nApna plan choose karo:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💸 Daily Plan ₹10":
        await update.message.reply_text("✅ Daily plan select hua\n\nPayment bhejo UPI pe: 9876543210@upi")
    
    elif text == "🔥 Weekly Plan ₹50":
        await update.message.reply_text("✅ Weekly plan select hua\n\nPayment bhejo UPI pe: 9876543210@upi")
    
    elif text == "👑 Monthly Plan ₹150":
        await update.message.reply_text("✅ Monthly plan select hua\n\nPayment bhejo UPI pe: 9876543210@upi")
    
    else:
        await update.message.reply_text("⚠️ Please menu se plan select karo")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing hai!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
