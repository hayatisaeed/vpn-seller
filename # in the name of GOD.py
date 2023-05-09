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
import json






keyboard = [
        ['ارسال فایل'],
        ['لیست کانال ها'],
        ['🌐 پیام همگانی']
    ]
admin_main_menu = ReplyKeyboardMarkup(keyboard)

cancel_keyboard = [
    ['🔙 انصراف و بازگشت']
]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)



def get_channels():
    with open('data.json', 'r') as f:
        data = json.load(f)['channels']
    return data

def get_users():
    with open('data.json', 'r') as f:
        data = json.load(f)['users']
    return data

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Data:
TOKEN = "5688074990:AAE3mAtJBxDyo30PmDJaN-Uf-3DlWofjymI"
ADMIN_ID = 5574109547 # must be integer
BOT_USERNAME = 'cucktooshbot'


async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass
async def del_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass
async def channels_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

        

async def is_member(user_id, CHANNEL_ID, context):
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if chat_member.status == ChatMember.MEMBER or chat_member.status == ChatMember.ADMINISTRATOR or chat_member.status == ChatMember.OWNER:
            return True
        else:
            return False
    except:
        return False

async def member_check(context, update):
    user_id = update.effective_user.id
    channels = get_channels()
    not_joined = []
    for CHANNEL_ID in channels:
        user_is_member = await is_member(user_id, CHANNEL_ID, context)
        if not user_is_member:
            not_joined.append([CHANNEL_ID, channels[CHANNEL_ID]])
    if len(not_joined) > 0:
        join_keyboard = []
        num = 1
        for i in not_joined:
            join_keyboard.append([InlineKeyboardButton(f"عضویت در کانال {num}", url=i[1])])
            num += 1
        join_keyboard.append([InlineKeyboardButton(f"عضو شدم ✅", callback_data='joined')])
        join_markup = InlineKeyboardMarkup(join_keyboard)
        if not context.user_data['sent_message']:
            message = await context.bot.send_message(chat_id=user_id, text="سلام. برای استفاده از خدمات این بات باید ابتدا در کانال های زیر عضو بشوید:", reply_markup=join_markup)
            context.user_data['sent_message'] = message.message_id
            context.user_data['message_id'] = message.message_id
        else:
            await context.bot.edit_message_text(chat_id=user_id, message_id=context.user_data['sent_message'], text="لطفا در کانال های زیر عضو شوید.")
            await context.bot.edit_message_reply_markup(chat_id=user_id, message_id=context.user_data['sent_message'], reply_markup=join_markup)
        return 0
    return 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    file_id = None
    context.user_data['sent_message'] = 0
    context.user_data['waiting_link'] = 0
    if len(context.args) > 0:
        file_id = context.args[0]
        context.user_data['waiting_link'] = f'https://t.me/{BOT_USERNAME}?start={file_id}'

    if not await member_check(context, update):
        return


    users = get_users()
    if user_id not in users:
        with open('data.json', 'r') as f:
            data = json.load(f)
        data['users'].append(user_id)
        with open('data.json', 'w') as f:
            json.dump(data, f)


    if file_id != None:
        try:
            await context.bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_ID, message_id=file_id)
        except:
            await context.bot.send_message(chat_id=user_id, text="متاسفانه این فایل حذف شده است.")
        return


    keyboard = [
        ['ارسال فایل'],
        ['لیست کانال ها'],
        ['🌐 پیام همگانی']
    ]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="Hello there!")
    if user_id == ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="Options:", reply_markup=markup)

async def joined_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.id
    if not await member_check(context, update):
        await context.bot.answer_callback_query(callback_query_id=query.id, text="شما هنوز عضو نشده اید ❌")
    else:
        await context.bot.answer_callback_query(callback_query_id=query.id, text="عضویت شما تایید شد ✅")
        context.user_data['sent_message'] = 0
        await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=context.user_data['message_id'])
        if str(user_id) != str(ADMIN_ID):
            if context.user_data['waiting_link']:
                try:
                    file_id = context.user_data['waiting_link']
                    await context.bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_ID, message_id=file_id)
                except:
                    await context.bot.send_message(chat_id=user_id, text="متاسفانه این فایل حذف شده است.")
            else:
                await context.bot.send_message(chat_id=user_id, text="سلام!")
        else:
            await context.bot.send_message(chat_id=user_id, text='Hello Admin!', reply_markup=admin_main_menu)



async def brodcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="شما ادمین نیستی برادر من. پیام همگانی میخوای بفرستی؟‌ :) خخخ")
        return ConversationHandler.END
    await context.bot.send_message(chat_id=user_id, text="حله!‌پیامت رو برام بفرست تا به همه شون فورواردش کنم", reply_markup=cancel_markup)
    return 'GET_MESSAGE'
async def brodcast_get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="شما ادمین نیستی برادر من. پیام همگانی میخوای بفرستی؟‌ :) خخخ")
        return ConversationHandler.END
    msg_id = update.message.message_id
    with open('data.json', 'r') as f:
        data = json.load(f)

    users = data['users']
    await context.bot.send_message(chat_id=user_id, text="در حال ارسال پیام برای همه ...")
    recivers_count = 0
    for user in users:
        try:
            await context.bot.copy_message(from_chat_id=user_id, chat_id=user, message_id=msg_id)
            recivers_count += 1
        except:
            pass
    await context.bot.send_message(chat_id=user_id, text=f"پیام برای {recivers_count} کاربر با موفقیت ارسال شد.", reply_markup=admin_main_menu)
    return ConversationHandler.END

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="Error.")
        return ConversationHandler.END
    await context.bot.send_message(chat_id=user_id, text="Ok. Send Me Your file.", reply_markup=cancel_markup)
    return 'GET_FILE'
async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    msg_id = update.message.message_id
    await context.bot.send_message(chat_id=user_id, text=f"https://t.me/{BOT_USERNAME}?start={msg_id}", reply_markup=admin_main_menu)
    return ConversationHandler.END


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if str(user_id) != str(ADMIN_ID):
        await update.message.reply_text('به منوی اصلی بازگشتید.')
        return ConversationHandler.END
    else:
        await update.message.reply_text('بازگشت به منوی اصلی ادمین', reply_markup=admin_main_menu)
        return ConversationHandler.END


async def send_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="Error.")
        return ConversationHandler.END
    channels = get_channels()
    msg = "Your Channels:\n\n\n"
    for ch in channels:
        msg += ch + ' ' + channels[ch] + '\n'
    msg += "\n\nSend me the new list."
    await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=cancel_markup)
    return 'GET_CHANNELS'
async def get_channels_names(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    ch_list = {}
    num = 1
    ch_txt = update.message.text.split()
    if len(ch_txt) % 2:
        await context.bot.send_message(chat_id=user_id, text="Wrong Pattern. Try Again.", reply_markup=cancel_markup)
        return 'GET_CHANNELS'
    i = 0
    while i < len(ch_txt):
        if num % 2 == 1:
            ch_list[ch_txt[num - 1]] =  ch_txt[num]
            num += 2
            i += 2
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['channels'] = ch_list
    with open('data.json', 'w') as f:
        json.dump(data, f)
    await context.bot.send_message(chat_id=user_id, text="Done.", reply_markup=admin_main_menu)
    return ConversationHandler.END


brodcast_message_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🌐 پیام همگانی$'), brodcast)],
        states={
            'GET_MESSAGE': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.ALL, brodcast_get_message)]
        },
        fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
)

send_file_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^ارسال فایل$'), send_file)],
    states={
        'GET_FILE': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.ALL, get_file)]
    },
    fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
)

edit_channels_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^لیست کانال ها$'), send_channels)],
    states={
        'GET_CHANNELS': [MessageHandler(~filters.Regex('^🔙 انصراف و بازگشت$') & filters.ALL, get_channels_names)]
    },
    fallbacks=[MessageHandler(filters.Regex('^🔙 انصراف و بازگشت$'), back_to_main_menu)]
)



# instances
application = Application.builder().token(TOKEN).build()
bot = telegram.Bot(token=TOKEN)


def main() -> None:
    start_handler = CommandHandler('start', start)
    joined_handler = CallbackQueryHandler(joined_check, pattern="^joined$")

    # ADD Handlers to Application
    application.add_handler(start_handler)
    application.add_handler(joined_handler)
    application.add_handler(brodcast_message_conv_handler)
    application.add_handler(send_file_conv_handler)
    application.add_handler(edit_channels_conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()