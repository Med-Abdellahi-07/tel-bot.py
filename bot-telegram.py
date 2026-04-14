import streamlit as st
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- واجهة ويب Streamlit ---
st.set_page_config(page_title="Telegram Bot Server", page_icon="🤖")
st.title("🤖 Bot En Ligne")
st.info("سيرفر البوت يعمل الآن في الخلفية.")

# --- جلب التوكن من الإعدادات السرية ---
# تأكد انك وضعت TOKEN في Secrets بموقع Streamlit
TOKEN = st.secrets["TOKEN"]

# --- بيانات البوت (قائمة الملفات والمستخدمين) ---
ALLOWED_USERS = ["ST25000", "ST25001", "ST25003"]

FILES = {
    "Algèbre linéaire et applications": {
        "Chapitre 1": "BQACAgQAAxkBAAOOaWuBmblWgyA53XWsBlQpoYvaVKkAApMrAAIDq2FTx1LXORVtlWs4BA",
        "TD 1": "BQACAgQAAxkBAAIBy2lt5QE23QrP0dtDDUjYDm1jgrB7AAJeHAACaQNxU9hnH7PrnsxsOAQ",
        "TD 2": "BQACAgQAAxkBAAIBzGlt5QFIT9DQVIquTdSQ1uHuJ7I8AAJfHAACaQNxUz9_ZPH9JqsYOAQ",
        "Livre": "BQACAgQAAxkBAAIB3mlt-WfrIVG0S-4rUnrM3xf_sC8VAAKBHAACaQNxUzmuUQah6mrZOAQ"
    },
    "Historique et enjeux de l'IA": {
        "Cours 1": "BQACAgQAAxkBAAIBt2lt4hHsQGSVX1tyvNOzK-ZHf2LHAAJZHAACaQNxU1RkY7kzA02IOAQ"
    },
    "Application de l'IA": {
        "Cours 1": "BQACAgQAAxkBAAOUaWuD0rwMI4LN_lE1R8N1i8GhCF8AApUrAAIDq2FTFd8kXqZ-JQs4BA",
        "Cours 2": "BQACAgQAAxkBAAOVaWuENcMCxmX7GS0nvlRTcle0nSsAApcrAAIDq2FTM8Ukmevx91k4BA"
    },
    "Algorithmiques": {
        "Cours 1": "BQACAgQAAxkBAAIBtWlt4HCByfV8M1I2tH8uLLgCcWbGAAJVHAACaQNxUxLAWmqhvNUBOAQ"
    },
    "Programmation Python": {
        "Cours 1": "BQACAgQAAxkBAAIBsmlt3qAX3Aw50-lh3UYFKBiYOsbfAAJMHAACaQNxU6fMj19Takg6OAQ",
        "Cours 2": "BQACAgQAAxkBAAIBsWlt3p4hIw8b1Oe8Z8BXHCnk9CKFAAJLHAACaQNxU9vV-K1nmUmPOAQ"
    },
    "Anglais": {
        "Niveau A1": "BQACAgQAAxkBAAIB3Wlt-JpxXq1VSepO0oBhCGOmqZzkAAJ-HAACaQNxU6Lp1d68aCGfOAQ",
        "Niveau A2": "BQACAgQAAxkBAAIB3Glt-GKd7qRSgESVktNdLzDee9KfAAJ9HAACaQNxU9lxQz5NH_IHOAQ"
    }
}

# --- وظائف البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً بك! يرجى إدخال الرقم التعريفي الخاص بك:")

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    if code in ALLOWED_USERS:
        keyboard = [[InlineKeyboardButton(subject, callback_data=subject)] for subject in FILES]
        await update.message.reply_text("✅ تم التحقق بنجاح\n📚 اختر المادة التي تريدها:", 
                                       reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ عذراً، هذا الرقم غير صحيح.")

async def choose_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data
    keyboard = [[InlineKeyboardButton(name, callback_data=f"{subject}|{name}")] for name in FILES[subject]]
    await query.message.reply_text(f"📘 مادة {subject}\nاختر الدرس:", reply_markup=InlineKeyboardMarkup(keyboard))

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject, lesson = query.data.split("|")
    file_id = FILES[subject][lesson]
    await query.message.reply_document(file_id)

# --- تشغيل المحرك ---

def run_bot():
    # بناء التطبيق
    application = ApplicationBuilder().token(TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user))
    application.add_handler(CallbackQueryHandler(choose_subject, pattern="^[^|]+$"))
    application.add_handler(CallbackQueryHandler(send_file, pattern=".+\\|.+"))

    # تشغيل البوت بدون إشارات النظام لتجنب أخطاء السيرفر
    application.run_polling(stop_signals=None)

# التأكد من عدم تكرار تشغيل البوت عند تحديث الصفحة
if 'bot_started' not in st.session_state:
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    st.session_state['bot_started'] = True
    st.success("✅ تم تشغيل البوت بنجاح وهو مستعد للعمل!")
