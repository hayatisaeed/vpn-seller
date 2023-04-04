# in the name of GOD.
import logging
from typing import Dict
import telegram
from telegram import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import datetime
import message_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# replace with your own
TOKEN = "6126767405:AAH4B-wx0ckT6NoMPp6pA3lGoGAU-DxEC9Q" # 6126767405:AAH4B-wx0ckT6NoMPp6pA3lGoGAU-DxEC9Q
ADMIN_ID = 1767064220 # integer
CHANNEL_ID = '@kard_vpn' # string, public id

# keyboards:
main_menu_keyboard = [
    ['خرید سرویس 🛒'],
    ['دریافت تست', 'آموزش اتصال'],
    ['ℹ️ اطلاعات حساب', '➕ افزایش موجودی'],
    ['🛡 سرویس‌های من'],
    ['👤 زیر مجموعه گیری'],
    ['📅 تاریخچه‌ی سفارشات'],
    ['پیام به پشتیبانی 👨‍💻', 'راهنمای بات'],
    ['🤝 پلن همکار']
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True)

# when the user starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    # First, add user data to databases (database_handler)
    # Then, check if user is joined to channel
    # Then send welcome message
    await update.message.reply_text('Hey there!', reply_markup=main_menu)

# instances
application = Application.builder().token(TOKEN).build()

def main() -> None:
    # Command & Conversation & CallbackQuery Handlers will take place here.
    start_handler = CommandHandler('start', start)

    # add handlers to the application
    application.add_handler(start_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()