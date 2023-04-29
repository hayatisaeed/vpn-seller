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
    filters
)
from telegram import ChatMember
import datetime
import database_handler

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
SEND_SUPPORT_MESSAGE = 0

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
        if chat_member.status == ChatMember.MEMBER or chat_member.status == ChatMember.ADMINISTRATOR or chat_member.status == ChatMember.OWNER:
            return True
        else:
            return False
    except:
        return False









# when the user starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if not await member_check(update, context):
        keyboard = [
            [InlineKeyboardButton('عضویت در کانال', url=f"https://t.me/{CHANNEL_ID[1:]}")],
            [InlineKeyboardButton('عضو شدم ✅', callback_data='joined')]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        msg = await update.message.reply_text(f'برای استفاده از خدمات بات باید در کانال ما عضو باشید\n{CHANNEL_ID}', reply_markup=markup)
        context.chat_data['message_id'] = msg.message_id
        return
    
    if database_handler.newUser(user_id):
        await context.bot.send_message(chat_id=user_id, text="سلام! به فروشگاه ما خوش اومدید! میتونید با استفاده از گزینه های زیر از امکانات بات استفاده کنید:", reply_markup=(main_menu if user_id != ADMIN_ID else admin_main_menu))
        if user_id != ADMIN_ID:
            buttons = [
                [InlineKeyboardButton('پیام', callback_data=f"reply_to_user {user_id}"), InlineKeyboardButton('مدیریت کاربر', callback_data=f'admin_user_panel {user_id}')],
                [InlineKeyboardButton('🔴مسدود کردن کاربر', callback_data=f"block_user {user_id}")]
            ]
            admin_markup = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"یک نوگل جدید باتو استارت کرد. \n آیدی عددیش: {user_id}", reply_markup=admin_markup)
    else:
        await context.bot.send_message(chat_id=user_id, text="بات راه اندازی مجدد شد. منوی اصلی:", reply_markup=(main_menu if user_id != ADMIN_ID else admin_main_menu))
    
    return ConversationHandler.END

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
async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.message.reply_text('اطلاعات اکانت شما به شرح زیر است:\nاطلاع ۱\nاطلاع ۲\n...', reply_markup=main_menu)

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if str(user_id) != str(ADMIN_ID):
        await update.message.reply_text('به منوی اصلی بازگشتید.', reply_markup=main_menu)
        return ConversationHandler.END
    else:
        await update.message.reply_text('بازگشت به منوی اصلی ادمین', reply_markup=admin_main_menu)
        return ConversationHandler.END

async def get_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.message.reply_text('شما در حال ارسال پیام به پشتیبانی هستید. لطفا متن پیام خود را بنویسید. \n', reply_markup=cancel_markup)
    return SEND_SUPPORT_MESSAGE

async def send_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    markup = ReplyKeyboardMarkup(main_menu_keyboard)
    buttons = [
        [InlineKeyboardButton('پاسخ', callback_data=f"reply_to_user {user_id}"), InlineKeyboardButton('مدیریت کاربر', callback_data=f'admin_user_panel {user_id}')],
        [InlineKeyboardButton('🔴مسدود کردن کاربر', callback_data=f"block_user {user_id}")]
    ]
    admin_markup = InlineKeyboardMarkup(buttons)
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        if update.message.caption:
            caption = update.message.caption
        else:
            caption = 'بدون توضیحات'
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file_id, caption=f"یک پیام جدید از کاربر {user_id}:\n\n\nمتن پیام:\n{caption}", reply_markup=admin_markup)
        await update.message.reply_text('پیام با موفقیت ارسال شد.', reply_markup=main_menu)
        return ConversationHandler.END
    elif update.message.text:
        txt = update.message.text
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"یک پیام جدید از کاربر {user_id}:\n\n\nمتن پیام:\n{txt}", reply_markup=admin_markup)
        await update.message.reply_text('پیام با موفقیت ارسال شد.', reply_markup=main_menu)
        return ConversationHandler.END
    await update.message.reply_text('🚫 پیام ارسال نشد. لطفا متن یا تصویر ارسال بفرمایید.', reply_markup=main_menu)
    return ConversationHandler.END

async def user_charge_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_credit = 10 # update by db
    keyboard = [
        ['20000', '30000', '40000', '50000'],
        ['60000', '70000', '80000', '90000'],
        ['100000', '200000', '500000'],
        ['1000000', '2000000'],
        ['انصراف و بازگشت']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=user_id, text=f"شما {user_credit} تومن توی حسابت داری. مقدار مدنظرت برای شارژ کردن رو از منوی پایین انتخاب کن یا عدد مدنظرت رو به لاتین وارد کن (همه‌ی اعداد به تومن هستن):", reply_markup=markup)
    return 'PRICE'
async def charge_get_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    price = update.message.text
    try:
        price = int(price)
    except:
        keyboard = [
            ['20000', '30000', '40000', '50000'],
            ['60000', '70000', '80000', '90000'],
            ['100000', '200000', '500000'],
            ['1000000', '2000000'],
            ['انصراف و بازگشت']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text='فقط عدد لاتین بفرست.', reply_markup=markup)
        return 'PRICE'
    context.user_data['charge_price'] = price
    card_number = 1234123412341234 # update by db
    card_owner = 'OWNER OF CARD' # update by db
    keyboard = [
        ['انصراف و بازگشت']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=user_id, text=f"👍حله. مبلغ {price} پس از واریز به کیف پول شما افزوده خواهد شد.\n\n\nلطفا {price} تومن به شماره کارت زیر واریز کرده و رسیدش رو به صورت تصویر یا متن برای بات بفرستید:\n\n\n🔰 شماره کارت: {card_number}\nبه نام: {card_owner}\n\n.", reply_markup=markup)
    return 'RESID'
async def charge_get_resid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    markup = ReplyKeyboardMarkup(main_menu_keyboard)
    buttons = [
        [InlineKeyboardButton('تایید ✅', callback_data=f"ok {user_id}"), InlineKeyboardButton('رد تراکنش ❌', callback_data=f'deny {user_id}')],
        [InlineKeyboardButton('پیام', callback_data=f"reply_to_user {user_id}"), InlineKeyboardButton('مدیریت کاربر', callback_data=f'admin_user_panel {user_id}')],
        [InlineKeyboardButton('🔴مسدود کردن کاربر', callback_data=f"block_user {user_id}")]
    ]
    admin_markup = InlineKeyboardMarkup(buttons)
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        if update.message.caption:
            caption = update.message.caption
        else:
            caption = 'بدون توضیحات'
        payment_id = update.message.message_id
        charge_price = context.user_data['charge_price']
        # update with db: add to database
        database_handler.newPayment(user_id, payment_id, charge_price)
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file_id, caption=f"🤑💲 دریافتی جدید از کاربر {user_id}:\n\nمبلغ: {charge_price} تومان\n\n آیدی تلگرامی: @{update.effective_user.username} \n\n\n\nتوضیحات رسید:\n{caption}", reply_markup=admin_markup)
        await update.message.reply_text(f'✅درخواست افزایش موجودی ارسال شد. بلافاصله پس از تایید ادمین موجودی شما افزایش خواهد یافت.\n\nشماره پیگیری:\n{user_id}-{payment_id}', reply_markup=main_menu)
        return ConversationHandler.END
    elif update.message.text:
        txt = update.message.text
        payment_id = update.message.message_id
        charge_price = context.user_data['charge_price']
        # update with db: add to database
        database_handler.newPayment(user_id, payment_id, charge_price)
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🤑💲 دریافتی جدید از کاربر {user_id}:\n\nمبلغ: {charge_price} تومان\n\n آیدی تلگرامی: @{update.effective_user.username} \n\n\n\nتوضیحات رسید:\n{txt}", reply_markup=admin_markup)
        await update.message.reply_text(f'✅درخواست افزایش موجودی ارسال شد. بلافاصله پس از تایید ادمین موجودی شما افزایش خواهد یافت.\n\nشماره پیگیری:\n{user_id}-{payment_id}', reply_markup=main_menu)
        return ConversationHandler.END
    await update.message.reply_text('🚫 رسید ارسال نشد. لطفا متن یا تصویر ارسال بفرمایید.', reply_markup=cancel_markup)
    return 'RESID'

async def show_packages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    packages_data = database_handler.getPackages()
    msg = 'packages:\n' # should be updated by database
    # buttons = [[InlineKeyboardButton('*', callback_data=f"none"), InlineKeyboardButton('عنوان', callback_data=f"none"), InlineKeyboardButton('اپراتور', callback_data=f"none"), InlineKeyboardButton('توضیحات', callback_data=f"none"), InlineKeyboardButton('قیمت', callback_data=f"none"), InlineKeyboardButton('خرید', callback_data=f"none")]]
    buttons = []
    for i in packages_data:
        # buttons.append([InlineKeyboardButton(i, callback_data=f"none"), InlineKeyboardButton(packages_data[i]['package_name'], callback_data=f"none"), InlineKeyboardButton(packages_data[i]['package_operator'], callback_data=f"none"), InlineKeyboardButton(packages_data[i]['package_description'], callback_data=f"none"), InlineKeyboardButton(packages_data[i]['package_price'], callback_data=f"none"), InlineKeyboardButton('خرید', callback_data=f"buy {i}")])
        buttons.append([InlineKeyboardButton(packages_data[i]['package_name'], callback_data=f"buy {i}")])
    buttons.append([InlineKeyboardButton('🔙 بازگشت', callback_data=f"main_menu")])
    inline_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=[inline_markup, main_menu])


#--- ADMIN ---#
async def brodcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def send_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass










# instances
application = Application.builder().token(TOKEN).build()
bot = bot = telegram.Bot(token=TOKEN)

def main() -> None:
    # Command & Conversation & CallbackQuery Handlers will take place here.
    start_handler = CommandHandler('start', start)

    joined_handler = CallbackQueryHandler(joined_check, pattern="^joined$")

    show_package_handler = MessageHandler(filters.Regex('^خرید سرویس 🛒$'), show_packages)

    send_support_message_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^پیام به پشتیبانی 👨‍💻$'), get_support_message)],
        states={
            SEND_SUPPORT_MESSAGE: [MessageHandler(filters.ALL & ~filters.Regex('^انصراف و بازگشت$'), send_support_message)]
        },
        fallbacks=[MessageHandler(filters.Regex('^انصراف و بازگشت$'), back_to_main_menu)]
    )

    charge_wallet_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^➕ افزایش موجودی$'), user_charge_wallet)],
        states={
            'PRICE': [MessageHandler(~filters.Regex('^انصراف و بازگشت$') & filters.TEXT, charge_get_price)],
            'RESID':[MessageHandler(~filters.Regex('^انصراف و بازگشت$') & filters.ALL, charge_get_resid)]
        },
        fallbacks=[MessageHandler(filters.Regex('^انصراف و بازگشت$'), back_to_main_menu)]
    )

    show_info_message_handler = MessageHandler(filters.Regex('^ℹ️ اطلاعات حساب$'), show_info)

    # reply_to_user_handler = CallbackQueryHandler(reply_to_user, )

    # add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(joined_handler)
    application.add_handler(show_info_message_handler)
    application.add_handler(send_support_message_conv_handler)
    application.add_handler(charge_wallet_conv_handler)
    application.add_handler(show_package_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()