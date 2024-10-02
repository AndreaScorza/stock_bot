from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from stock_bot.config import Config
from stock_bot.handlers import handle_new_user
from stock_bot.db import init_db
import logging

class TelegramBot:
    def __init__(self):
        # Initialize the bot with the token using the new Application builder
        self.application = Application.builder().token(Config.BOT_TOKEN).build()

    async def start(self, update: Update, context):
        chat_id = update.effective_chat.id
        username = update.effective_chat.username or "Unknown"
        
        # Handle new users joining
        handle_new_user(chat_id, username)
        
        # Send a welcome message
        await context.bot.send_message(chat_id=chat_id, text="Welcome to the bot!")

    def run(self):
        # Add a command handler for the /start command
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        # Start polling for updates
        self.application.run_polling()

def main():
    # Initialize the database
    init_db()

    # Run the bot
    bot = TelegramBot()
    bot.run()

if __name__ == "__main__":
    main()
