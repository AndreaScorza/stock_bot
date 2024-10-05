import asyncio
import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler
from stock_bot.config import Config
from stock_bot.db_handler import handle_new_user
from stock_bot.db import init_db
from stock_bot.transaction_handler import TransactionHandler
from stock_bot.notification_handler import NotificationHandler


class TelegramBot:
    def __init__(self):
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        self.notifier = NotificationHandler(self.application.bot)
        self.tx_handler = TransactionHandler()

    async def start(self, update: Update):
        chat_id = update.effective_chat.id
        username = update.effective_chat.username or "Unknown"
        
        logging.info(f"Received /start command from user {username} (chat_id={chat_id})")

        is_new_user = handle_new_user(chat_id, username)
        
        if is_new_user:
            logging.info(f"New user {username} added to the database.")
            await self.notifier.send_welcome_message(chat_id)
        else:
            logging.info(f"User {username} is already registered.")
            await self.notifier.send_already_registered_message(chat_id)


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
        
        # Custom asyncio-based scheduling loop
        while True:
            # Run the job every 30 minutes (1800 seconds)
            logging.info("Scheduling next job...")
            await self.async_job()  # Run the asynchronous job
            await asyncio.sleep(60)  # Non-blocking sleep for 30 minutes

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

    # Get the existing event loop and run the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())  # Use the event loop to run the bot


if __name__ == "__main__":
    main()
