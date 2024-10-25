#This main.py 
import os
import logging
from multiprocessing import Process
from app import app  # استيراد تطبيق Flask من ملف app.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from info import BOT_TOKEN
from commands import ban, restrict, unrestrict, unban, unknown
from replies import reply_to_yabot, reply_to_bot, reply_to_name
from reveal import reveal
from filter import add_filters
from pin import pin_message, pin_message_with_notification, pin_message_with_duration, add_pin_handlers

# إعدادات تسجيل الأحداث
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# أمر الترحيب عند استخدام /start
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "مرحبًا، أنا بوت ركيزةَ مصمم لإدارة مجموعات التليجرام.\n\n"
        "ما أقدمه:\n\n"
        "منع الإعلانات بجميع أشكالها:\n"
        "• ضمن الرسائل النصية 📄\n"
        "• ضمن الروابط 📎\n\n"
        "الحماية من:\n"
        "• الإرهاب والتطرف\n"
        "• المحتوى الإباحي 🔞\n"
        "• الحسابات الوهمية (البوتات) عبر الحظر أو التقييد\n\n"
        "وأيضًا العديد من المزايا الأخرى التي تسهم في حماية وتسريع إدارة مجموعتك.\n\n"
        "للاستفسار والتفعيل، تواصل معي عبر: @Y305F"
    )
    keyboard = [
        [InlineKeyboardButton("المطور", url='https://t.me/Y305F')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'^(طرد|حظر)$'), ban))
    application.add_handler(MessageHandler(filters.Regex(r'^(قيد)$'), restrict))
    application.add_handler(MessageHandler(filters.Regex(r'^(إلغاء القيد)$'), unrestrict))
    application.add_handler(MessageHandler(filters.Regex(r'يابوت'), reply_to_yabot))
    application.add_handler(MessageHandler(filters.Regex(r'بوت'), reply_to_bot))
    application.add_handler(MessageHandler(filters.Regex(r'لاتزودها'), reply_to_name))
    application.add_handler(MessageHandler(filters.Regex(r'^(كشف)$'), reveal))
    application.add_handler(MessageHandler(filters.Regex(r'^(إلغاء الحظر)$'), unban))

    
    # إضافة معالجات لتثبيت الرسائل
    add_pin_handlers(application)
    # إضافة فلتر الرسائل
    add_filters(application)

    # بدء تشغيل البوت
    application.run_polling()

def run_flask():
    flask_port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host='0.0.0.0', port=flask_port, use_reloader=False, debug=True)

if __name__ == '__main__':
    # تشغيل Flask و Telegram bot في عمليات منفصلة
    flask_process = Process(target=run_flask)
    bot_process = Process(target=run_bot)
    
    flask_process.start()
    bot_process.start()
    
    flask_process.join()
    bot_process.join()
