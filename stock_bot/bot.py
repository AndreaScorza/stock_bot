from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from stock_bot.config import Config
from stock_bot.handlers import handle_new_user
from stock_bot.db import init_db
from stock_bot.transaction_handler import TransatcionHandler  # Import your scraper class
from stock_bot.notification_handler import NotificationHandler
import schedule
import time
import logging

class TelegramBot:
    def __init__(self):
        # Initialize the bot with the token using the new Application builder
        self.application = Application.builder().token(Config.BOT_TOKEN).build()

        
        # Pass the initialized bot to the NotificationHandler
        self.notifier = NotificationHandler(self.application.bot)  # Pass the bot object


        # Initialize the transaction scraper (which handles scraping and notifications)
        self.tx_handler = TransatcionHandler()

    async def start(self, update: Update, context):
        chat_id = update.effective_chat.id
        username = update.effective_chat.username or "Unknown"
        
        # Handle new users joining and check if the user is new
        is_new_user = handle_new_user(chat_id, username)
        
        if is_new_user:
            # Send a welcome message only if the user is new
            self.notifier.send_welcome_message(chat_id)
        else:
            # Optionally, do something else if the user is already present
            print(f"User {username} is already registered.")


    def schedule_tasks(self):
        # Schedule the job to run every 30 minutes
        schedule.every(30).minutes.do(self.tx_handler.fetch_and_store)

        # Keep the script running and checking the schedule
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        # Add a command handler for the /start command
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        # Start polling for updates (Telegram messages)
        self.application.run_polling()

        # Start the scheduled scraping task
        self.schedule_tasks()

def main():
    # Initialize the database
    init_db()

    # Run the bot
    bot = TelegramBot()
    bot.run()

if __name__ == "__main__":
    main()
