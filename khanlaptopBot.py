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
import logging

# Configure logging for better debugging and monitoring
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot settings - Use environment variables or config file in production
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY_HERE'
ADMIN_ID = 123456789  # Replace with your admin Telegram user ID
FORCE_JOIN_CHANNEL = '@your_channel_username'  # Channel users must join

# Connect to OpenAI
openai.api_key = OPENAI_API_KEY

# Inline buttons for quick actions
def get_inline_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 View Products", url="https://your-website.com")],
        [InlineKeyboardButton("📞 Phone Consultation", callback_data="phone_consult")]
    ])

# Persistent keyboard buttons at the bottom
def get_persistent_keyboard():
    return ReplyKeyboardMarkup(
        [['📞 Phone Consultation'], ['🛍 Products', '❓ Help']],
        resize_keyboard=True
    )

# Check if user is a member of the required channel
async def is_user_member(context, user_id):
    try:
        member = await context.bot.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        return False

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_user_member(context, user_id):
        await update.message.reply_text(
            "To use the bot, please join our channel first 👇\nhttps://t.me/your_channel_username"
        )
        return
    await update.message.reply_text(
        "Welcome! Please select one of the options below 👇",
        reply_markup=get_inline_buttons()
    )

# Handle inline button clicks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "phone_consult":
        await query.message.reply_text(
            "Please enter your name and contact number so we can reach out. 📞"
        )

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    # Handle persistent keyboard selections
    if text == "📞 Phone Consultation":
        await update.message.reply_text("Please enter your name and contact number. 📱")
        return
    elif text == "🛍 Products":
        await update.message.reply_text("Check out our products here: https://your-website.com")
        return
    elif text == "❓ Help":
        await update.message.reply_text("How can I assist you? Ask about products, consultations, or general queries.")
        return
    
    # If message likely contains a phone number (basic check), forward to admin
    if len(text) >= 7 and any(char.isdigit() for char in text):
        msg = f"📞 New phone consultation request:\n\n👤 Name: {user.first_name} @{user.username or 'No username'}\n📝 Message:\n{text}"
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
            await update.message.reply_text("✅ Your information has been received. We'll contact you soon.")
        except Exception as e:
            logger.error(f"Error sending message to admin: {e}")
            await update.message.reply_text("❌ Error processing your request. Please try again.")
        return
    
    # Send query to GPT for product consultation
    await update.message.reply_text("Analyzing suitable options...⏳")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional product consultant. Suggest the best options based on user needs and available inventory."},
                {"role": "user", "content": f"{text}\nPlease suggest based on the product list."}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        await update.message.reply_text("❌ Error getting response from AI. Please try again.")

# Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Bot is running.")
    app.run_polling()
