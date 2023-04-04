# in the name of GOD.
import telegram
from telegram import *
from telegram.ext import *
import datetime
import message_handler

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
def start(update, context):
    user_id = update.effective_user.id
    # First, add user data to databases (database_handler)
    # Then, check if user is joined to channel
    # Then send welcome message
    context.bot.send_message(chat_id=user_id, text="Hey there!", reply_markup=main_menu)

# instances
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)

def main():
    # Command & Conversation & CallbackQuery Handlers will take place here.

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()