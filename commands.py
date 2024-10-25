from telegram import ChatPermissions, Update
from telegram.ext import CallbackContext

# دالة لطرد عضو
async def ban(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None

    if user_id is None:
        await update.message.reply_text("يرجى الرد على رسالة العضو الذي تريد طرده أو تحديده باستخدام @username أو id.")
        return

    try:
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text("تم طرد العضو بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء طرد العضو: {str(e)}")

# دالة لتقييد عضو
async def restrict(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None

    if user_id is None:
        await update.message.reply_text("يرجى الرد على رسالة العضو الذي تريد تقييده أو تحديده باستخدام @username أو id.")
        return

    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_manage_topics=False
    )

    try:
        await update.effective_chat.restrict_member(user_id, permissions)
        await update.message.reply_text("تم تقييد العضو بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء تقييد العضو: {str(e)}")

# دالة لإلغاء تقييد عضو
async def unrestrict(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None

    if user_id is None:
        await update.message.reply_text("يرجى الرد على رسالة العضو الذي تريد إلغاء تقييده أو تحديده باستخدام @username أو id.")
        return

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_manage_topics=True
    )

    try:
        await update.effective_chat.restrict_member(user_id, permissions)
        await update.message.reply_text("تم إلغاء تقييد العضو بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء إلغاء تقييد العضو: {str(e)}")

# دالة لإلغاء حظر عضو
async def unban(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None

    if user_id is None:
        await update.message.reply_text("يرجى الرد على رسالة العضو الذي تريد إلغاء حظره أو تحديده باستخدام @username أو id.")
        return

    try:
        await update.effective_chat.unban_member(user_id)
        await update.message.reply_text("تم إلغاء حظر العضو بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء إلغاء حظر العضو: {str(e)}")

# دالة للتعامل مع الأوامر غير المعروفة
async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("عذرًا، لم أتعرف على هذا الأمر.")
