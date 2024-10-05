import asyncio
import logging
from telegram.ext import Application
from stock_bot.config import Config
from stock_bot.db import init_db
from stock_bot.transaction_handler import TransactionHandler
from stock_bot.notification_handler import NotificationHandler

class TransactionBot:
    def __init__(self):
        # Initialize the bot application
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Initialize transaction handler and notifier with a valid bot instance
        self.tx_handler = TransactionHandler()
        self.notifier = NotificationHandler(self.application.bot)

    async def async_job(self):
        logging.info("Executing scheduled job: Fetching and storing transactions...")
        new_transactions = self.tx_handler.fetch_and_store()

        if new_transactions:
            logging.info(f"Found {len(new_transactions)} new transactions. Notifying users...")
            await self.notifier.notify_users(new_transactions)
        else:
            logging.info("No new transactions found.")

    async def schedule_tasks_async(self):
        logging.info("Starting the scheduling task")
        
        while True:
            logging.info("Scheduling next job...")
            await self.async_job()  # Run the asynchronous job and await it
            await asyncio.sleep(1800)  # Non-blocking sleep for 30 minutes

    async def run(self):
        logging.info("Initializing the Application...")
        # Explicitly initialize the application
        await self.application.initialize()

        logging.info("Starting scheduled tasks...")
        await self.schedule_tasks_async()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    init_db()

    bot = TransactionBot()

    # Get the existing event loop and run the scheduled tasks
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())

if __name__ == "__main__":
    main()
