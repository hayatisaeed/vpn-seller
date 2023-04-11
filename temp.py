from telegram.ext import Updater, CommandHandler
import logging

# Enable logging 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 
logger = logging.getLogger(__name__) 
  
# Define a function to check if the user is subscribed to the channel 
def check_subscription(bot, update): 

    # Get the list of users subscribed to the channel 
    subscribers = bot.get_chat_members_count('@channel_name') 

    # Check if the user is in the list of subscribers 
    if update.message.from_user in subscribers: 

        # Do function A if user is subscribed 
        update.message.reply_text("You are subscribed!") 

    else: 

        # Do function B if user is not subscribed  
        update.message.reply_text("You are not subscribed!")  

  
# Create an Updater object and attach dispatcher to it 
updater = Updater('TOKEN')   # Replace 'TOKEN' with your bot token  
dispatcher = updater.dispatcher  

 # Add command handler to dispatcher  
dispatcher.add_handler(CommandHandler('check', check_subscription))  

 # Start the bot  
updater.start_polling()

