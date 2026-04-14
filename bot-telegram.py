import streamlit as st
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد واجهة الويب
st.title("Bot En Ligne")
st.write("Le bot Telegram est en cours d'exécution en arrière-plan.")

# جلب التوكن بأمان من Secrets
TOKEN = st.secrets["TOKEN"]

ALLOWED_USERS = ["ST25000", "ST25001", "ST25003"]
FILES = {
    "Algèbre linéaire": {"Chapitre 1": "BQACAgQAAxkBAAOOaWuBmblWgyA53XWsBlQpoYvaVKkAApMrAAIDq2FTx1LXORVtlWs4BA"},
    "Python": {"Cours 1": "BQACAgQAAxkBAAIBsmlt3qAX3Aw50-lh3UYFKBiYOsbfAAJMHAACaQNxU6fMj19Takg6OAQ"}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً بك! يرجى إدخال الرقم التعريفي الخاص بك:")

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    if code in ALLOWED_USERS:
        keyboard = [[InlineKeyboardButton(s, callback_data=s)] for s in FILES]
        await update.message.reply_text("✅ تم التحقق بنجاح! اختر المادة التي تريدها:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ عذراً، هذا الرقم غير صحيح. يرجى التأكد منه.")

async def run_bot():
    # بناء التطبيق باستخدام التوكن السري
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة الأوامر والمستقبلات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user))
    
    # تشغيل البوت بطريقة متوافقة مع Streamlit و Asyncio
    await app.initialize()
    await app.start_polling()
    await asyncio.Event().wait()

if __name__ == '__main__':
    # تشغيل الحلقة البرمجية لتجنب تضارب الـ Threads
    try:
        asyncio.run(run_bot())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
