import streamlit as st
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# واجهة الويب
st.title("Bot En Ligne")
st.write("Le bot Telegram est en cours d'exécution...")

# جلب التوكن من Secrets
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
        await update.message.reply_text("✅ تم التحقق! اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ الرقم غير صحيح.")

def run_bot():
    # إنشاء التطبيق
    application = ApplicationBuilder().token(TOKEN).build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user))

    # تشغيل البوت مع تعطيل التعامل مع إشارات النظام لتجنب RuntimeError
    application.run_polling(stop_signals=None)

# التحقق مما إذا كان البوت يعمل بالفعل لكي لا نشغل أكثر من نسخة
if 'bot_started' not in st.session_state:
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    st.session_state['bot_started'] = True
    st.success("تم تشغيل محرك البوت بنجاح!")
