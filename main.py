# in the name of GOD.
import logging
from typing import Dict
import telegram
from telegram import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram import ChatMember
import datetime

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# replace with your own
TOKEN = "6126767405:AAH4B-wx0ckT6NoMPp6pA3lGoGAU-DxEC9Q" # 6126767405:AAH4B-wx0ckT6NoMPp6pA3lGoGAU-DxEC9Q
ADMIN_ID = 1767064220 # integer
CHANNEL_ID = '@kard_vpn_test' # string, public id

# Constants:
CHOOSING = range(1)
ENSERAF, SEND_SUPPORT_MESSAGE = 0, 1

# keyboards:
main_menu_keyboard = [
    ['خرید سرویس 🛒'],
    ['دریافت تست', 'آموزش اتصال'],
    ['ℹ️ اطلاعات حساب', '➕ افزایش موجودی'],
    ['🛡 سرویس‌های من', '👤 زیر مجموعه گیری', '📅 تاریخچه‌ی سفارشات'],
    ['پیام به پشتیبانی 👨‍💻', 'راهنمای بات'],
    ['🤝 پلن همکار']
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True)

admin_menu_keyboard = [
    ['admin_alaki']
]
admin_main_menu = ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True)

cancel_keyboard = [
    ['انصراف و بازگشت']
]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)

# channel lock (must be joint to channel)
async def member_check(update, context):
    user_id = update.effective_user.id
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if chat_member.status == ChatMember.MEMBER or chat_member.status == ChatMember.ADMINISTRATOR or chat_member.status == ChatMember.CREATOR:
            return True
        else:
            return False
    except:
        return False


# when the user starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    # First, add user data to databases (database_handler)
    if not await member_check(update, context):
        keyboard = [
            [InlineKeyboardButton('عضویت در کانال', url=f"https://t.me/{CHANNEL_ID[1:]}")],
            [InlineKeyboardButton('عضو شدم ✅', callback_data='joined')]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        msg = await update.message.reply_text(f'برای استفاده از خدمات بات باید در کانال ما عضو باشید\n{CHANNEL_ID}', reply_markup=markup)
        context.chat_data['message_id'] = msg.message_id
        return
    # Then send welcome message
    if str(user_id) != str(ADMIN_ID):
        await update.message.reply_text('Hey there!', reply_markup=main_menu)
    else:
        await update.message.reply_text('Hello Admin!', reply_markup=admin_main_menu)

# when the user clicks on 'عضو شدم' button
async def joined_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    query = update.callback_query
    if not await member_check(update, context):
        await context.bot.answer_callback_query(callback_query_id=query.id, text="شما هنوز عضو نشده اید ❌")
    else:
        await context.bot.answer_callback_query(callback_query_id=query.id, text="عضویت شما تایید شد ✅")
        await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=context.chat_data['message_id'])
        if str(user_id) != str(ADMIN_ID):
            await context.bot.send_message(chat_id=user_id, text='سلام! به ربات کارد خوش اومدید ☺️ لطفا از بین گزینه های زیر یکی رو انتخاب کنید:', reply_markup=main_menu)
        else:
            await context.bot.send_message(chat_id=user_id, text='Hello Admin!', reply_markup=admin_main_menu)


#--- Functions ---#

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if str(user_id) != str(ADMIN_ID):
        await update.message.reply_text('به منوی اصلی بازگشتید.', reply_markup=main_menu)
    else:
        await update.message.reply_text('بازگشت به منوی اصلی ادمین', reply_markup=admin_main_menu)

async def get_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.message.reply_text('شما در حال ارسال پیام به پشتیبانی هستید. لطفا متن پیام خود را بنویسید.', reply_markup=cancel_markup)
    return SEND_SUPPORT_MESSAGE

async def send_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    markup = InlineKeyboardMarkup(main_menu_keyboard)
    buttons = [
        [InlineKeyboardButton('پاسخ به این کاربر', callback_data=f"reply_to_user {user_id}")],
        [InlineKeyboardButton('مدیریت این کاربر', callback_data=f'admin_user_panel {user_id}')]
    ]
    admin_markup = InlineKeyboardMarkup(markup)
    await context.bot.copy_message(from_chat_id=user_id, chat_id=ADMIN_ID, message_id=update.message.message_id, reply_markup=admin_markup)
    await update.message.reply_text('پیام با موفقیت ارسال شد.', reply_markup=main_menu)


# instances
application = Application.builder().token(TOKEN).build()
bot = bot = telegram.Bot(token=TOKEN)

def main() -> None:
    # Command & Conversation & CallbackQuery Handlers will take place here.
    joined_handler = CallbackQueryHandler(joined_check, pattern="^joined$")
    send_support_message_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^پیام به پشتیبانی 👨‍💻$'), get_support_message)],
        states={
            ENSERAF: MessageHandler(filters.Regex('^انصراف و بازگشت$'), back_to_main_menu),
            SEND_SUPPORT_MESSAGE: MessageHandler(~filters.Command, send_support_message)
        },
        fallbacks=[]
    )

    # add handlers to the application
    application.add_handler(joined_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()