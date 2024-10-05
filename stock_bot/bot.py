from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from stock_bot.config import Config
from stock_bot.handlers import handle_new_user
from stock_bot.db import init_db
from stock_bot.transaction_handler import TransactionHandler  # Import your scraper class
from stock_bot.notification_handler import NotificationHandler
import schedule
import time
import asyncio
import logging


class TelegramBot:
    def __init__(self):
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        self.notifier = NotificationHandler(self.application.bot)
        self.tx_handler = TransactionHandler()

    async def start(self, update: Update):
        chat_id = update.effective_chat.id
        username = update.effective_chat.username or "Unknown"
        
        is_new_user = handle_new_user(chat_id, username)
        
        if is_new_user:
            self.notifier.send_welcome_message(chat_id)
        else:
            logging.info(f"User {username} is already registered.")

    async def schedule_tasks_async(self):
        logging.info("Starting the scheduling task")

        def job():
            logging.info("Executing scheduled job: Fetching and storing transactions...")
            new_transactions = self.tx_handler.fetch_and_store()

            if new_transactions:
                logging.info(f"Found {len(new_transactions)} new transactions. Notifying users...")
                self.notifier.notify_users(new_transactions)
            else:
                logging.info("No new transactions found.")

        # Schedule the job to run every 30 minutes
        schedule.every(30).minutes.do(job)

        while True:
            schedule.run_pending()
            await asyncio.sleep(1)  # Non-blocking sleep

    async def run(self):
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        logging.info("Initializing the Application...")
        # Explicitly initialize the application
        await self.application.initialize()

        logging.info("Starting Telegram polling and scheduling tasks")

        # Run both polling and scheduling in parallel using asyncio
        await asyncio.gather(
            self.application.start(),
            self.schedule_tasks_async()
        )

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    init_db()
    bot = TelegramBot()
    
    # asyncio.run(bot.run())

        # Get the existing event loop and run the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())  # Use the event loop to run the bot

if __name__ == "__main__":
    main()
