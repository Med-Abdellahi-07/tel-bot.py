import threading
import streamlit as st
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# إعداد واجهة ويب بسيطة لإبقاء السيرفر يعمل
st.title("Bot En Ligne")
st.write("Le bot Telegram est en cours d'exécution en arrière-plan.")

TOKEN = "8145989681:AAFfeCUpbxNGnC6g3g44IEUS3bKh4vt7JZU" # ضع التوكن الخاص بك هنا
ALLOWED_USERS = ["ST25000", "ST25001", "ST25003"]
FILES = {
    "Algèbre linéaire": {"Chapitre 1": "BQACAgQAAxkBAAOOaWuBmblWgyA53XWsBlQpoYvaVKkAApMrAAIDq2FTx1LXORVtlWs4BA"},
    "Python": {"Cours 1": "BQACAgQAAxkBAAIBsmlt3qAX3Aw50-lh3UYFKBiYOsbfAAJMHAACaQNxU6fMj19Takg6OAQ"}
}

async def start(update, context):
    await update.message.reply_text("👋 أدخل الرقم التعريفي:")

async def check_user(update, context):
    code = update.message.text.strip()
    if code in ALLOWED_USERS:
        keyboard = [[InlineKeyboardButton(s, callback_data=s)] for s in FILES]
        await update.message.reply_text("✅ تم التحقق! اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ رقم غير صحيح")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user))
    app.run_polling()

# تشغيل البوت في خلفية (Thread)
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()