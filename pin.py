import re
import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters

# دالة لتثبيت الرسالة
async def pin_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message = update.message.reply_to_message

    # التحقق من أن المستخدم هو مشرف
    if not (await context.bot.get_chat_member(chat_id, update.effective_user.id)).status in ['administrator', 'creator']:
        await update.message.reply_text("عذرًا، هذا الأمر مخصص للمشرفين فقط.")
        return

    if not message:
        await update.message.reply_text("يرجى الرد على الرسالة التي تريد تثبيتها.")
        return

    try:
        await context.bot.pin_chat_message(chat_id, message.message_id, disable_notification=False)
        await update.message.reply_text("تم تثبيت الرسالة بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

# دالة لتثبيت الرسالة بدون إشعار
async def pin_message_with_notification(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message = update.message.reply_to_message

    # التحقق من أن المستخدم هو مشرف
    if not (await context.bot.get_chat_member(chat_id, update.effective_user.id)).status in ['administrator', 'creator']:
        await update.message.reply_text("عذرًا، هذا الأمر مخصص للمشرفين فقط.")
        return

    if not message:
        await update.message.reply_text("يرجى الرد على الرسالة التي تريد تثبيتها.")
        return

    try:
        await context.bot.pin_chat_message(chat_id, message.message_id, disable_notification=True)
        await update.message.reply_text("تم تثبيت الرسالة بدون إشعار.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

# دالة لتثبيت الرسالة بمدة معينة
async def pin_message_with_duration(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message = update.message.reply_to_message
    command_text = update.message.text.split(maxsplit=2)

    # التحقق من أن المستخدم هو مشرف
    if not (await context.bot.get_chat_member(chat_id, update.effective_user.id)).status in ['administrator', 'creator']:
        await update.message.reply_text("عذرًا، هذا الأمر مخصص للمشرفين فقط.")
        return

    if not message:
        await update.message.reply_text("يرجى الرد على الرسالة التي تريد تثبيتها.")
        return

    if len(command_text) < 2:
        await update.message.reply_text("يرجى إدخال المدة ووحدة الوقت بعد الأمر.")
        return

    duration_text = command_text[1]
    notify = '!' in command_text[0]

    # تحويل المدة إلى ثوانٍ
    duration_seconds = parse_duration(duration_text)
    if duration_seconds is None:
        await update.message.reply_text("صيغة المدة غير صحيحة. يرجى استخدام صيغ مثل '5 دقيقة' أو '2 ساعة'.")
        return

    try:
        await context.bot.pin_chat_message(chat_id, message.message_id, disable_notification=not notify)
        await update.message.reply_text(f"تم تثبيت الرسالة {'بإشعار' if notify else 'بدون إشعار'} لمدة {duration_text}.")
        
        # تأخير لمدة التثبيت ثم إزالة التثبيت
        await asyncio.sleep(duration_seconds)
        await context.bot.unpin_chat_message(chat_id, message.message_id)
        await update.message.reply_text("تم إزالة تثبيت الرسالة بعد انتهاء المدة المحددة.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

# دالة لتحليل المدة
def parse_duration(duration_text: str) -> int:
    duration_pattern = re.compile(r'(\d+)\s*(دقيقة|د|ساعة|س|يوم|ي)')
    match = duration_pattern.match(duration_text)
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if unit in ['دقيقة', 'د']:
        return value * 60
    elif unit in ['ساعة', 'س']:
        return value * 3600
    elif unit in ['يوم', 'ي']:
        return value * 86400
    return None

# دالة لإضافة معالجات الأوامر المتعلقة بتثبيت الرسائل
def add_pin_handlers(application) -> None:
    application.add_handler(MessageHandler(filters.Regex(r'^ثبت(\s.*)?$'), pin_message))
    application.add_handler(MessageHandler(filters.Regex(r'^ثبت!(\s.*)?$'), pin_message_with_notification))
    application.add_handler(MessageHandler(filters.Regex(r'^ثبت(\s.*)$'), pin_message_with_duration))
