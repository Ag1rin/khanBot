from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import openai

# 🛠 تنظیمات ربات
TELEGRAM_BOT_TOKEN = ''
OPENAI_API_KEY = ''
ADMIN_ID = 51514121
FORCE_JOIN_CHANNEL = "@"

# 🔐 اتصال به OpenAI
openai.api_key = OPENAI_API_KEY

# 🎛 دکمه‌های شیشه‌ای
def get_inline_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 مشاهده محصولات", url="https://khanlaptop.ir")],
        [InlineKeyboardButton("📞 مشاوره تلفنی", callback_data="phone_consult")]
    ])

# ⌨️ دکمه‌های دائمی پایین صفحه
def get_persistent_keyboard():
    return ReplyKeyboardMarkup(
        [['📞 مشاوره تلفنی'], ['🛍 محصولات', '❓ راهنما']],
        resize_keyboard=True
    )

# ✅ بررسی عضویت کاربر در کانال
async def is_user_member(context, user_id):
    try:
        member = await context.bot.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_user_member(context, user_id):
        await update.message.reply_text(
            "برای استفاده از ربات لطفاً ابتدا در کانال ما عضو شوید 👇\nhttps://t.me/khanlaptop"
        )
        return

    await update.message.reply_text(
        "خوش آمدی! لطفاً یکی از گزینه‌های زیر را انتخاب کن 👇",
        reply_markup=get_inline_buttons()
    )

# 📲 هندل کردن کلیک روی دکمه‌های شیشه‌ای
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "phone_consult":
        await query.message.reply_text(
            "لطفاً نام و شماره تماس خود را وارد کنید تا با شما تماس بگیریم. 📞"
        )

# 💬 هندل کردن پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user

    # دکمه مشاوره تلفنی فشرده شده
    if text == "📞 مشاوره تلفنی":
        await update.message.reply_text("لطفاً نام و شماره تماس خود را وارد کنید. 📱")
        return

    # اگر پیام شامل شماره تلفن بود، بفرست برای ادمین
    if len(text) >= 7 and any(char.isdigit() for char in text):
        msg = f"📞 درخواست مشاوره تلفنی جدید:\n\n👤 نام: {user.first_name} @{user.username or 'بدون آیدی'}\n📝 پیام:\n{text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text("✅ اطلاعات شما دریافت شد. به زودی با شما تماس خواهیم گرفت.")
        return

    # 👨‍💻 ارسال به GPT برای مشاوره خرید
    await update.message.reply_text("در حال بررسی گزینه‌های مناسب...⏳")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "شما یک مشاور حرفه‌ای خرید لپ‌تاپ هستید. بر اساس نیاز کاربر و موجودی فروشگاه، بهترین گزینه را پیشنهاد بده."},
                {"role": "user", "content": f"{text}\nلطفاً با توجه به لیست محصولات پیشنهاد بده."}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت پاسخ از هوش مصنوعی. لطفاً دوباره تلاش کنید.")
        print(e)

# ▶️ اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ربات KhanLaptopBot روشن شد.")
    app.run_polling()
