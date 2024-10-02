from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
from stock_bot.config import Config
from stock_bot.handlers import handle_new_user
from stock_bot.db import init_db

class TelegramBot:
    def __init__(self):
        # Initialize the bot with the token
        self.bot = Bot(token=Config.BOT_TOKEN)
        self.updater = Updater(token=Config.BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start(self, update: Update, context):
        chat_id = update.effective_chat.id
        username = update.effective_chat.username or "Unknown"
        
        # Handle new users joining
        handle_new_user(chat_id, username)
        
        # Send a welcome message
        context.bot.send_message(chat_id=chat_id, text="Welcome to the bot!")

    def run(self):
        # Add a command handler for the /start command
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        # Start polling for updates
        self.updater.start_polling()

if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Run the bot
    bot = TelegramBot()
    bot.run()
