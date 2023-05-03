# in the name of GOD.
import logging
from typing import Dict
import telegram
from telegram import *
# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     CallbackQueryHandler,
#     ContextTypes,
#     ConversationHandler,
#     MessageHandler,
#     filters
# )
from telegram import *
from telegram.ext import *
from telegram import ChatMember
import datetime
import prettytable as pt
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
    ['خرید سرویس 🛒', 'دریافت تست'],
    ['پیام به پشتیبانی 👨‍💻', '➕ افزایش موجودی'],
    ['آموزش اتصال', 'راهنمای بات'],
    ['🛡 سرویس‌های من', 'ℹ️ اطلاعات حساب'],
    ['👤 زیر مجموعه گیری', '🤝 پلن همکار'],
    ['📆 تاریخچه‌ی پرداخت‌ها']
]
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True)

admin_menu_keyboard = [
    ['🌐 پیام همگانی', '📊 آمار'],
    ['🧾 لیست کاربران', '👤 مدیریت کاربر'],
    ['ارسال کانفیگ', '📦 پلن ها'],
    ['⚙️ تنظیمات ربات']
]
admin_main_menu = ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True)

cancel_keyboard = [
    ['🔙 انصراف و بازگشت']
]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)

user_manage_keyboard = [
    ['📨 پیام', '💳 موجودی'],
    ['⛔️ بلاک / آنبلاک', '🤝 همکار / عادی', ],
    ['🧮 درصد پرداختی', '📅 تاریخچه پرداخت'],
    ['🗑 حذف کاربر', '🔄 تایید تراکنش'],
    ['🔙 انصراف و بازگشت']
]
user_manage_markup = ReplyKeyboardMarkup(user_manage_keyboard, one_time_keyboard=True)


bot_setting_keyboard = [
    ['📣 کانال ها', '🤝 کمیسیون'],
    ['🧪 کانفیگ تست', '💬 پیام های بات'],
    ['🔋 بکاپ دیتابیس', '💡روشن / خاموش 🔴'],
    ['🔙 انصراف و بازگشت']
]
bot_setting_markup = ReplyKeyboardMarkup(bot_setting_keyboard, one_time_keyboard=True)

setting_commission_keyboard = [
    ['کارمزد استارت', 'درصد از خرید'],
    ['لیست استثنا', '👤 کمیسیونرها'],
    ['🔙 انصراف و بازگشت']
]
setting_commission_markup = ReplyKeyboardMarkup(setting_commission_keyboard, one_time_keyboard=True)

setting_channels_keyboard = [

]
setting_channels_markup = ''

setting_messages_keyboard = [

]
setting_messages_markup = ''

setting_test_keyboard = [

]
setting_test_markup = ''




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
    data = database_handler.userInfo(user_id)
    msg = f'ℹ️ اطلاعات اکانت شما به شرح زیر است: \n\n🆔 آیدی عددی شما: ```{user_id}```\n💰 موجودی: {data['credit']} تومان\n{'% درصد پرداخت:' + str(data['percent']) + '\n' if data['percent'] != 100 else ''}{'🤝 وضعیت همکاری: همکار\n' if data['is_hamkar']}✋ وضعیت انسداد: {'بلاک شده ⛔️' if data['is_blocked'] else 'آزاد ✅'}\n🏃‍♂ تعداد زیر مجموعه: {data['number_of_invited']}\n\n.'
    await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=main_menu)

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
        ['🔙 انصراف و بازگشت']
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
            ['🔙 انصراف و بازگشت']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text='فقط عدد لاتین بفرست.', reply_markup=markup)
        return 'PRICE'
    context.user_data['charge_price'] = price
    card_number = 1234123412341234 # update by db
    card_owner = 'OWNER OF CARD' # update by db
    keyboard = [
        ['🔙 انصراف و بازگشت']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=user_id, text=f"👍حله. مبلغ {price} پس از واریز به کیف پول شما افزوده خواهد شد.\n\n\nلطفا {price} تومن به شماره کارت زیر واریز کرده و رسیدش رو به صورت تصویر یا متن برای بات بفرستید:\n\n\n🔰 شماره کارت: {card_number}\nبه نام: {card_owner}\n\n.", reply_markup=markup)
    return 'RESID'
async def charge_get_resid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    markup = ReplyKeyboardMarkup(main_menu_keyboard)
    buttons = [
        [InlineKeyboardButton('تایید ✅', callback_data=f"ok {user_id}-{update.message.message_id}"), InlineKeyboardButton('رد تراکنش ❌', callback_data=f'deny {user_id}-{update.message.message_id}')],
        [InlineKeyboardButton('مسدود کردن کاربر ⛔️', callback_data=f"block_user {user_id}")]
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
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file_id, caption=f"🤑💲 دریافتی جدید از کاربر {user_id}:\n\n💲 مبلغ: {charge_price} تومان\n\n🆔 آیدی تلگرامی: @{update.effective_user.username} \n\n\n\n🔢 شماره تراکنش: {payment_id}\n\n💬 توضیحات رسید:\n{caption}", reply_markup=admin_markup)
        await update.message.reply_text(f'✅درخواست افزایش موجودی ارسال شد. بلافاصله پس از تایید ادمین موجودی شما افزایش خواهد یافت.\n\nشماره پیگیری:\n{user_id}-{payment_id}', reply_markup=main_menu)
        return ConversationHandler.END
    elif update.message.text:
        txt = update.message.text
        payment_id = update.message.message_id
        charge_price = context.user_data['charge_price']
        # update with db: add to database
        database_handler.newPayment(user_id, payment_id, charge_price)
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🤑💲 دریافتی جدید از کاربر {user_id}:\n\n💲 مبلغ: {charge_price} تومان\n\n🆔 آیدی تلگرامی: @{update.effective_user.username} \n\n\n\n🔢 شماره تراکنش: {payment_id}\n\n💬 توضیحات رسید:\n{txt}", reply_markup=admin_markup)
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
    await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=inline_markup)


#--- ADMIN ---#
async def brodcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="شما ادمین نیستی برادر من. پیام همگانی میخوای بفرستی؟‌ :) خخخ")
        return ConversationHandler.END
    keyboard = [
        ['🤝 فقط همکارها', '👤 فقط کاربرای عادی'],
        ['برای همه'],
        ['🔙 انصراف و بازگشت']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="حله. برای کدوم دسته میخوای پیام بفرستی؟", reply_markup=reply_markup)
    return 'GET_PEOPLE'
async def brodcast_get_people(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="شما ادمین نیستی برادر من. پیام همگانی میخوای بفرستی؟‌ :) خخخ", reply_markup=main_menu)
        return ConversationHandler.END
    people = update.message.text
    if people == '🤝 فقط همکارها':
        context.user_data['people'] = 'Hamkar'
        await context.bot.send_message(chat_id=user_id, text="حله! پیامت رو فقط برای همکار ها میفرستم.\n\n پیامی که میخوای براشون بفرستم رو بفرست واسم.", reply_markup=cancel_markup)
    elif people == '👤 فقط کاربرای عادی':
        context.user_data['people'] = 'Normal'
        await context.bot.send_message(chat_id=user_id, text="حله! پیامت رو فقط برای کاربرای عادی میفرستم.\n\n پیامی که میخوای واسشون بفرستم رو بفرست واسم.", reply_markup=cancel_markup)
    elif people == 'برای همه':
        context.user_data['people'] = 'All'
        await context.bot.send_message(chat_id=user_id, text="حله! برای همه میفرستم.\n\n پیامی که میخوای واسشون بفرستم رو بفرست واسم.", reply_markup=cancel_markup)
    else:
        keyboard = [
            ['🤝 فقط همکارها', '👤 فقط کاربرای عادی'],
            ['برای همه'],
            ['🔙 انصراف و بازگشت']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=user_id, text="متوجه نشدم، برای چه کسی؟", reply_markup=reply_markup)
        return 'GET_PEOPLE'
    return 'GET_MESSAGE'
async def brodcast_get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="شما ادمین نیستی برادر من. پیام همگانی میخوای بفرستی؟‌ :) خخخ")
        return ConversationHandler.END
    msg_id = update.message.message_id
    users = database_handler.getUsers(context.user_data['people'])
    await context.bot.send_message(chat_id=user_id, text=f"در حال ارسال پیام برای دسته‌ی {context.user_data['people']} ...")
    recivers_count = 0
    for user in users:
        try:
            await context.bot.copy_message(from_chat_id=user_id, chat_id=user, message_id=msg_id)
            recivers_count += 1
        except:
            pass
    await context.bot.send_message(chat_id=user_id, text=f"پیام برای {recivers_count} کاربر از دسته‌ی {context.user_data['people']} با موفقیت ارسال شد.", reply_markup=admin_main_menu)
    return ConversationHandler.END


async def manage_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="دسترسی نداری به این بخش دادا. تلاش نکن بی خودی.", reply_markup=main_menu)
        return ConversationHandler.END
    await context.bot.send_message(chat_id=user_id, text="آیدی کاربر رو بفرست تا پنل مدیریتیشو برات باز کنم:", reply_markup=cancel_markup)
    return 'GET_ID'
async def show_manage_user_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="دسترسی نداری به این بخش دادا. تلاش نکن بی خودی.", reply_markup=main_menu)
        return ConversationHandler.END
    try:
        user_panel_id = int(update.message.text)
        user_data = database_handler.userInfo(user_panel_id)
        user_percent = user_data['percent']
        user_is_hamkar = user_data['is_hamkar']
        user_credit = user_data['credit']
        user_inviter = user_data['inviter']
        user_number_of_invited = user_data['number_of_invited']
        user_is_blocked = user_data['is_blocked']
        if user_is_blocked:
            blocked_text = 'مسدود شده 🖐'
        else:
            blocked_text = 'آزاد 🕊'
        msg = f"ℹ️ اطلاعات کاربر {user_panel_id} به شرح زیر است: \n\n\n💰 موجودی: {user_credit} تومان\n🧮 درصد پرداختی: {user_percent}\n🤝 وضعیت همکاری: {'همکار ✅' if user_is_hamkar else 'کاربر عادی'}\n✋ وضعیت انسداد: {'مسدود ⛔️' if user_is_blocked else 'آزاد 🟢'}\n🤵‍♂️ معرف: {'ندارد' if user_inviter == 0 else user_inviter}\n🏃‍♂ تعداد زیر مجموعه: {user_number_of_invited}\n\n\n چه کنم ❓"
        await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=user_manage_markup)
        context.user_data['manage_user_id'] = user_panel_id
        return 'GET_COMMAND'
    except:
        await context.bot.send_message(chat_id=user_id, text=f"هیچ یوزری با مشخصات زیر پیدا نشد\n\n\n{update.message.text}\n\n دوباره بفرست آیدیشو.", reply_markup=cancel_markup)
        return 'GET_ID'

async def user_manage_get_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="دسترسی نداری به این بخش دادا. تلاش نکن بی خودی.", reply_markup=main_menu)
        return ConversationHandler.END
    lst = []
    for i in user_manage_keyboard:
        for j in i:
            lst.append(j)
    msg = update.message.text
    if msg not in lst:
        await context.bot.send_message(chat_id=user_id, text="متوجه نشدم، چیکار کنم؟ (از منوی پایین انتخاب کن)", reply_markup=user_manage_markup)
        return 'GET_COMMAND'
    else:
        manage_user_id = context.user_data['manage_user_id']
        if msg == '📨 پیام':
            await context.bot.send_message(chat_id=user_id, text=f"در حال ارسال پیام برای {manage_user_id}\n\nلطفا متن پیامت رو بنویس:", reply_markup=cancel_markup)
            return 'GET_MESSAGE'
        if msg == '💳 موجودی':
            await context.bot.send_message(chat_id=user_id, text=f"در حال تعیین موجودی برای {manage_user_id} هستی.\n\n💰 موجودی فعلیش: {database_handler.userInfo(manage_user_id)['credit']} تومان\n\n\nموجودیش چقدر باید باشه؟")
            return 'GET_CREDIT'
        if msg == '🤝 همکار / عادی':
            try:
                user_is_hamkar = int(database_handler.userInfo(manage_user_id)['is_hamkar'])
                await context.bot.send_message(chat_id=user_id, text=f"این یوزر در حال حاضر همکار {'هست' if user_is_hamkar else 'نیست'} \n در حال تغییر وضعیتش ...")
                try:
                    database_handler.editUser(manage_user_id, 'is_hamkar', (0 if user_is_hamkar else 1))
                    await context.bot.send_message(chat_id=user_id, text="وضعیتش تغییر کرد. حالا چیکار کنم؟", reply_markup=user_manage_markup)
                    await context.bot.send_message(chat_id=manage_user_id, text=f"{'شما از اکنون دیگر به عنوان همکار شناخته نمیشوید. 👋' if user_is_hamkar else 'وضعیت همکاری شما به همکار تغییر کرد. سلام همکار 🤝'}")
                    return 'GET_COMMAND'
                except:
                    await context.bot.send_message(chat_is=user_id, text="خطایی رخ داده است.", reply_markup=user_manage_markup)
                    return 'GET_COMMAND'
            except:
                pass
            return 'GET_COMMAND'
        if msg == '🧮 درصد پرداختی':
            user_percent = int(database_handler.userInfo(manage_user_id)['percent'])
            await context.bot.send_message(chat_id=user_id, text=f"🧮 درصد پرداختی فعلی این کاربر: {user_percent}\n\n بکنمش چند درصد؟", reply_markup=cancel_markup)
            return 'GET_PERCENT'
        if msg == '📅 تاریخچه پرداخت':
            try:
                payment_log = database_handler.getPayment(manage_user_id)
                if payment_log == []:
                    await context.bot.send_message(chat_id=user_id, text="✖️ این کاربر تا کنون هیچ پرداختی انجام نداده.", reply_markup=user_manage_markup)
                    return 'GET_COMMAND'
                table = pt.PrettyTable(['id', '💲', '🆗'])
                table_data = []
                for i in payment_log:
                    table_data.append((str(i), payment_log[i]['price'], payment_log[i]['status']))
                for idd, price, status in table_data:
                    if status == 'ok':
                        status = '✅'
                    elif status == 'waiting':
                        status = '🟡'
                    elif status == 'denied':
                        status = '❌'
                    table.add_row([idd, price, status])
                await context.bot.send_message(chat_id=user_id, text=f"🧾 اطلاعات پرداخت این کاربر به شرح زیر است: \n\n\n<pre>{table}</pre>", parse_mode=constants.ParseMode.HTML, reply_markup=user_manage_markup)
                return 'GET_COMMAND'
            except:
                await context.bot.send_message(chat_id=user_id, text="خطایی رخ داده است.", reply_markup=user_manage_markup)
                return 'GET_COMMAND'
        if msg == '⛔️ بلاک / آنبلاک':
            try:
                user_is_blocked = int(database_handler.userInfo(manage_user_id)['is_blocked'])
                await context.bot.send_message(chat_id=user_id, text=f"این یوزر در حال حاضر بلاک {'هست ⛔️' if user_is_blocked else 'نیست ✅'} \n در حال تغییر وضعیتش ...")
                try:
                    database_handler.editUser(manage_user_id, 'is_blocked', (0 if user_is_blocked else 1))
                    await context.bot.send_message(chat_id=user_id, text="وضعیتش تغییر کرد. حالا چیکار کنم؟", reply_markup=user_manage_markup)
                    await context.bot.send_message(chat_id=manage_user_id, text=f"{'شما از بلاک بودن خارج شدید و میتوانید به پشتیبانی پیام ارسال کنید ✅' if user_is_blocked else 'شما توسط ادمین بلاک شده اید. دیگر نمیتوانید به پشتیبانی پیام ارسال کنید ⛔️'}")
                    return 'GET_COMMAND'
                except:
                    await context.bot.send_message(chat_is=user_id, text="خطایی رخ داده است.", reply_markup=user_manage_markup)
                    return 'GET_COMMAND'
            except:
                pass
        if msg == '🗑 حذف کاربر':
            await context.bot.send_message(chat_id=user_id, text="✖️ در حال حاضر امکان حذف کاربر وجود ندارد.", reply_markup=user_manage_markup)
            return 'GET_COMMAND'
        await context.bot.send_message(chat_id=user_id, text="دریافت شد تمام.", reply_markup=admin_main_menu)
        return ConversationHandler.END


async def send_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="دادا نمیتونی از این استفاده کنی. ارور بمولا", reply_markup=main_menu)
        return ConversationHandler.END
    msg_id = update.message.message_id
    try:
        await context.bot.copy_message(from_chat_id=ADMIN_ID, chat_id=context.user_data['manage_user_id'], message_id=msg_id)
        manage_user_id = context.user_data['manage_user_id']
        msg = f'پیامت ارسال شد.\n دیگه چه امری راجع به {manage_user_id} داری؟'
        await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=user_manage_markup)
    except:
        msg = f'☹️ متاسفانه به دلایلی پیامت ارسال نشد.\n\nUserID: {manage_user_id}\n\nدیگه چه امری داری؟'
        await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=user_manage_markup)
    return 'GET_COMMAND' 

async def set_user_credit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="دادا نمیتونی از این استفاده کنی. ارور بمولا", reply_markup=main_menu)
        return ConversationHandler.END
    try:
        uid = context.user_data['manage_user_id']
        val = int(update.message.text)
        try:
            database_handler.editUser(uid, 'credit', val)
            await context.bot.send_message(chat_id=user_id, text="موجودی تغییر کرد. دیگه چه کنم؟", reply_markup=user_manage_markup)
            await context.bot.send_message(chat_id=uid, text=f"💰 موجودی جدید: {val} تومان")
            return 'GET_COMMAND'
        except:
            await context.bot.send_message(chat_id=user_id, text="خطایی رخ داده، کل عملیات رو لغو کردم.", reply_markup=admin_main_menu)
            return ConversationHandler.END
    except:
        await context.bot.send_message(chat_id=user_id, text="عدد لاتین بفرست:", reply_markup=cancel_markup)
        return 'GET_CREDIT'
    await context.bot.send_message(chat_id=user_id, text="منوی اصلی:", reply_markup=admin_main_menu)
    return ConversationHandler.END

async def get_user_percent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="دادا نمیتونی از این استفاده کنی. ارور بمولا", reply_markup=main_menu)
        return ConversationHandler.END
    uid = context.user_data['manage_user_id']
    try:
        percent = int(update.message.text)
        if percent > 100 or percent < 0:
            await context.bot.send_message(chat_id=user_id, text="لطفا فقط یک عدد لاتین بین 0 و 100 بفرست", reply_markup=cancel_markup)
            return 'GET_PERCENT'
        database_handler.editUser(uid, 'percent', percent)
        await context.bot.send_message(chat_id=user_id, text="انجام شد. دیگه چه امری داری؟", reply_markup=user_manage_markup)
        await context.bot.send_message(chat_id=uid, text=f"🧮 شما از این به بعد {percent} درصد از هزینه ها را پرداخت خواهید کرد.")
        return 'GET_COMMAND'
    except:
        await context.bot.send_message(chat_id=user_id, text="لطفا فقط یک عدد لاتین بین 0 و 100 بفرست", reply_markup=cancel_markup)
        return 'GET_PERCENT'
    await context.bot.send_message(chat_id=user_id, text="خطایی رخ داده است. فرایند انجام نشد.", reply_markup=user_manage_markup)
    return 'GET_COMMAND'

async def show_user_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="⛔️ شما ادمین نیستید. \n دسترسی به این بخش برای شما غیر مجاز است.", reply_markup=main_menu)
        return
    data = database_handler.getUsers("All")
    hamkar_msg = '🤝 لیست همکاران به شرح زیر است:\n\n'
    normal_msg = '👤 لیست کاربران عادی به شرح زیر است: \n\n'

    for i in data:
        if data[i]['is_hamkar'] == 1:
            hamkar_msg += f'👉 ```{i}``` -> @{data[i]['user_name']}\n'
        else:
            normal_msg += f'👉 ```{i}``` -> @{data[i]['user_name']}\n'
    
    await context.bot.send_message(chat_id=user_id, text=hamkar_msg, reply_markup=admin_main_menu)
    await context.bot.send_message(chat_id=user_id, text=normal_msg, reply_markup=admin_main_menu)


async def show_setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="⛔️ شما به این بخش دسترسی ندارید ⛔️", reply_markup=main_menu)
        return ConversationHandler.END
    await context.bot.send_message(chat_id=user_id, text="⚙️ تنظیمات بات:", reply_markup=bot_setting_markup)
    return 'GET_COMMAND'
async def setting_get_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="⛔️ شما به این بخش دسترسی ندارید ⛔️", reply_markup=main_menu)
        return ConversationHandler.END
    await context.bot.send_message(chat_id=user_id, text="به زودی انشاءالله", reply_markup=admin_main_menu)
    return ConversationHandler.END

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
            SEND_SUPPORT_MESSAGE: [MessageHandler(filters.ALL & ~filters.Regex('^🔙 انصراف و بازگشت$'), send_support_message)]
        },
        fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
    )

    charge_wallet_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^➕ افزایش موجودی$'), user_charge_wallet)],
        states={
            'PRICE': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.TEXT, charge_get_price)],
            'RESID':[MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.ALL, charge_get_resid)]
        },
        fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
    )

    brodcast_message_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🌐 پیام همگانی$'), brodcast)],
        states={
            'GET_PEOPLE': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.TEXT, brodcast_get_people)],
            'GET_MESSAGE': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.TEXT, brodcast_get_message)]
        },
        fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
    )

    user_manage_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^👤 مدیریت کاربر$'), manage_user)],
        states={
            'GET_ID': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.TEXT, show_manage_user_panel)],
            'GET_COMMAND': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.TEXT, user_manage_get_command)],
            'GET_MESSAGE': [MessageHandler(filters.ALL & ~filters.Regex('^🔙 انصراف و بازگشت$'), send_user_message)],
            'GET_CREDIT': [MessageHandler(filters.ALL & ~filters.Regex('^🔙 انصراف و بازگشت$'), set_user_credit)],
            'GET_PERCENT': [MessageHandler(filters.ALL & ~filters.Regex('^🔙 انصراف و بازگشت$'), get_user_percent)],
        },
        fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
    )

    bot_setting_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^⚙️ تنظیمات ربات$'), show_setting)],
        states={
            'GET_COMMAND': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.TEXT, setting_get_command)]
        },
        fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
    )

    show_info_message_handler = MessageHandler(filters.Regex('^ℹ️ اطلاعات حساب$'), show_info)
    show_user_list_handler = MessageHandler(filters.Regex('^🧾 لیست کاربران$'), show_user_list)
    
    # reply_to_user_handler = CallbackQueryHandler(reply_to_user, )

    # add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(joined_handler)
    application.add_handler(show_info_message_handler)
    application.add_handler(send_support_message_conv_handler)
    application.add_handler(charge_wallet_conv_handler)
    application.add_handler(show_package_handler)
    application.add_handler(brodcast_message_conv_handler)
    application.add_handler(user_manage_conv_handler)
    application.add_handler(show_user_list_handler)
    application.add_handler(bot_setting_conv_handler)


    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()