import logging
import re
from telegram import Update, ChatMember
from telegram.ext import CallbackContext, MessageHandler, filters

# إعدادات تسجيل الأحداث
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قائمة الكلمات التي يجب تصفيتها
FORBIDDEN_WORDS = [
    "967", "بحوث", "+966", "عمل", "لتواصل", "للتواصل", "التواصل",
    "تعقيب", "خدمات", "النحو", "عرض خاص", "عرض", "+20", "فريق متخصص",
    "للحجز", "لطلب", "فوري", "سجل تجاري", "cv", "تكليف", "طلبة", "صّحًتٌــــــيَ",
    "سعوده", "سعودة", "مسيار", "المسيار", "اتواصل واتساب", "مــ ـرافق", "فحصـ",
    "إعلانات تجارية", "تواصل مباشر", "طلب عروض", "وظائف شاغرة", "توظيف", "تسويق",
    "مبيعات", "استفسار", "حجز", "معلومات حول", "إعلان", "إعلانات", "عرض ترويجي",
    "اتصال", "للاستفسار", "تواصل معنا", "فرص عمل", "مقابلات", "سيرة ذاتية", "آجآزهہ‌",
    "رعاية", "تأمين", "مؤسسة", "مشاريع", "اتصال بنا", "إعلانات الشركات", "صـ.ــحـتي" ,"واتـ ـساب", 
    "عروض خاصة", "خدمات طلابية", "عروض ترويجية", "بحث عمل", "وظيفة شاغرة", "فرصة عمل", "إعلانات توظيف",
    "تقديم طلب", "استفسار عن", "معلومات حول", "بدون إذن", "تقــ ـريـ ـر", "جـ.ازة",
    "اسقاط", "سكليف", "تطبيق صحتي", "كرت تشغيل", "ذي تحل", "ذا يحل", "القطـ.ـاعات",
    "خطابه", "الخطــابه", "whatsapp.com", "+967", "967", "قروض بن التنمية", "بنك التنمية", "سنرد", "وسنرد",
    "عذر طبي معتمد", "فحص طبي", "عذر طبي ورقي", "تقرير طبي ورقي", "ســ.ـكـلـ.ــيـ.ـف", "صــحـ.ـتــي",
    "شهادات صحية", "طاقم التدريس", "ذوو خبرة" ,"إجــ  ـازة" , "مــ ـرضــ ـية" ,"صــ ـحـ.ـتي"
    "التواصل واتساب", "يتوفر لدينا", "شهادة صحية", "مختوم pdf", "ارسال المعلومات واتس", "سِــکْــلَيَـــفُ"
]

# المستخدم المسموح به
ALLOWED_USERNAME = '@Raghdah1'

def remove_tashkeel(text):
    return re.sub(r'[\u0610-\u061A\u064B-\u0652]', '', text)

def normalize_arabic_text(text):
    # إزالة الحروف الإضافية مثل الشدة والمد وغيرها
    text = re.sub(r'[ـ*]', '', text)
    # إزالة المسافات المكررة
    text = re.sub(r'\s+', ' ', text).strip()

    # تحويل الحروف المشابهة
    normalization_map = {
        'ة': 'ه',
        'ى': 'ي',
        'آ': 'ا',
        'إ': 'ا',
        'أ': 'ا',
    }
    text = ''.join(normalization_map.get(char, char) for char in text)
    text = re.sub(r'\bال', '', text)
    text = re.sub(r'(.)\1+', r'\1', text)  # إزالة التكرار الزائد في الحروف
    text = re.sub(r'س+ل+ا+م+م* ع+ل+ي+ك+م*', 'السلام عليكم', text)  # تصحيح جملة السلام
    text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)

    text = remove_tashkeel(text)
    
    return text

def contains_forbidden_content(text):
    normalized_text = normalize_arabic_text(text)
    normalized_forbidden_words = [normalize_arabic_text(word) for word in FORBIDDEN_WORDS]

    for word in normalized_forbidden_words:
        if re.search(rf'\b{re.escape(word)}\b', normalized_text): 
            return True
        
    if re.search(r'(\+?20[1-9][0-9]{8,9})', normalized_text):  # أرقام مصرية
        return True
    if re.search(r'(\+?967[1-9][0-9]{7})', normalized_text):  # أرقام يمنية
        return True

    # التحقق من التركيبات المحظورة
    forbidden_combinations = [
        (r'\bاجازة مرضيه\b', r'\bتقرير طبي\b'), 
        (r'\bتقرير طبي\b', r'\bاجازة مرضيه\b'),
        (r'\bتكاليف\b', r'\bبرزنتيشن\b'),
        (r'\bعروض\b', r'\bمضمون\b'),
        (r'\bبوربوينت\b', r'\bواجبات\b'),
        (r'\bباوربوينت\b', r'\bواجبات\b'),
        (r'\bبوربوينت\b', r'\bمشاريع\b'),
        (r'\bباوربوينت\b', r'\bمشاريع\b'),
        (r'\bحل\b', r'\bخرائط مفاهيم\b'),
        (r'\bمشروع\b', r'\bتكاليف\b'),
        (r'\bحل\b', r'\bمضمون\b'),
        (r'\bامتحان\b', r'\bمشروع\b'), 
        (r'\bمشروع\b', r'\bامتحان\b'),
        (r'\bمضمون\b', r'\bيستاهل\b'),
        (r'\bيستاهل\b', r'\مضمون\b'),
    ]
    
    for pattern1, pattern2 in forbidden_combinations:
        if re.search(f'{pattern1}.*{pattern2}|{pattern2}.*{pattern1}', normalized_text):
            return True

    if re.search(r'http[s]?://|www\.|t\.me/|@\w+|wa\.me/\d+', normalized_text):
        return True

    return False

async def filter_messages(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.message.chat

    if chat.type not in ['group', 'supergroup']:
        return

    if user.is_bot:
        return

    try:
        chat_member = await context.bot.get_chat_member(chat.id, user.id)
    except Exception as e:
        logger.error(f"Error fetching chat member: {e}")
        return

    if chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        return

    message_text = update.message.text

    if ALLOWED_USERNAME in message_text:
        return

    if contains_forbidden_content(message_text):
        try:
            await update.message.delete()
            await update.message.reply_text("تم حذف الرسالة لاحتوائها على محتوى غير مسموح به.")
        except Exception as e:
            logger.error(f"Error deleting message: {e}")

async def handle_update(update: Update, context: CallbackContext) -> None:
    if update.message is not None:
        await filter_messages(update, context)
    elif update.edited_message is not None:
        edited_text = update.edited_message.text
        if contains_forbidden_content(edited_text):
            try:
                await context.bot.delete_message(chat_id=update.edited_message.chat.id, message_id=update.edited_message.message_id)
                await context.bot.send_message(chat_id=update.edited_message.chat.id, text="تم حذف الرسالة المعدلة لاحتوائها على محتوى غير مسموح به.")
            except Exception as e:
                logger.error(f"Error deleting edited message: {e}")

def add_filters(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_update))
