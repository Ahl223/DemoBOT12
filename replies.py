#This replies.py
from telegram import Update
from telegram.ext import CallbackContext

# تابع للرد على "يابوت"
async def reply_to_yabot(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text.lower()
    if 'يابوت' in message_text:
        await update.message.reply_text("تفضل، معك البوت")

# تابع للرد على "بوت"
async def reply_to_bot(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text.lower()
    if 'بوت' in message_text:
        await update.message.reply_text("مراقب 24/7!")

# تابع للرد على "ما اسمك" أو "ايش اسمك"
async def reply_to_name(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text.lower()
    if 'زودتها' in message_text or 'لاتزودها' in message_text:
        await update.message.reply_text("اسسف:")
