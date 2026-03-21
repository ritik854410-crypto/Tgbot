import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = "8662531601:AAGFiF1cDC2hbvfgQOfG1RASW7KZmiG8HCY"
ADMIN_ID = 8255274063  
UPI_ID = "74845725@axl" # Apni UPI ID yahan dalo or ye kaam naa kre to 
ritik.0073-7@waaxis ispe krna.
# --- PLANS DATA ---
# Yahan apne har plan ka alag Telegram link dalo
PLANS_DATA = {
    "149": {"name": "₹149 (800+ Vids)", "link": "https://t.me/+LINK_149_WALA"},
    "199": {"name": "₹199 (1000+ Vids)", "link": "https://t.me/+LINK_199_WALA"},
    "249": {"name": "₹249 (1500+ Vids)", "link": "https://t.me/+LINK_249_WALA"},
    "349": {"name": "₹349 (2500+ Vids)", "link": "https://t.me/+LINK_349_WALA"},
    "499": {"name": "₹499 (4000+ Vids)", "link": "https://t.me/+LINK_499_WALA"}
}

# QR Code Image Link (Agar aapke paas direct link nahi hai, toh bot sirf UPI ID dikhayega)
# Aap apni QR image ko kisi private channel mein bhej kar uska link yahan dal sakte hain
QR_IMAGE_URL = "https://your-qr-image-link.com/qr.jpg" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for amount, info in PLANS_DATA.items():
        keyboard.append([InlineKeyboardButton(info["name"], callback_data=f"plan_{amount}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Swagat hai! Kaunsa plan lena chahte hain?", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    plan_key = query.data.split("_")[1]
    context.user_data['selected_plan'] = plan_key
    
    msg = f"✨ Aapne select kiya: *{PLANS_DATA[plan_key]['name']}*\n\n" \
          f"👇 Niche diye gaye UPI/QR par payment karein:\n" \
          f"📍 UPI ID: `{UPI_ID}`\n\n" \
          "📸 *Payment ke baad screenshot isi bot ko bhejein.*"

    # Agar QR link hai toh photo bhejega, nahi toh sirf text
    try:
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=QR_IMAGE_URL, caption=msg, parse_mode='Markdown')
    except:
        await query.edit_message_text(text=msg, parse_mode='Markdown')

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        user = update.message.from_user
        photo_id = update.message.photo[-1].file_id
        plan_key = context.user_data.get('selected_plan', 'None')
        
        if plan_key == 'None':
            await update.message.reply_text("❌ Pehle koi plan select karein, phir screenshot bhejein.")
            return

        # Admin Approval Buttons
        keyboard = [
            [InlineKeyboardButton("✅ Approve", callback_data=f"app_{user.id}_{plan_key}"),
             InlineKeyboardButton("❌ Reject", callback_data=f"rej_{user.id}")]
        ]
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"🚨 *NEW PAYMENT REQUEST*\nUser: {user.first_name}\nPlan: ₹{plan_key}\nID: {user.id}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        await update.message.reply_text("⏳ Screenshot mil gaya! Admin check karke aapko link bhej denge.")

async def admin_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("_")
    action, user_id = data[0], int(data[1])

    if action == "app":
        plan_key = data[2]
        link = PLANS_DATA[plan_key]["link"]
        await context.bot.send_message(chat_id=user_id, text=f"🎉 Approve ho gaya! Aapka Link: {link}")
        await query.edit_message_caption(caption="✅ Approved & Link Sent!")
    else:
        await context.bot.send_message(chat_id=user_id, text="❌ Payment reject ho gaya. Sahi screenshot bhejein.")
        await query.edit_message_caption(caption="❌ Rejected!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click, pattern="^plan_"))
    app.add_handler(CallbackQueryHandler(admin_approval, pattern="^(app|rej)_"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    app.run_polling()

if __name__ == '__main__':
    main()
    
