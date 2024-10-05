from stock_bot.db_handler import get_all_users  # Import the function from handlers
import logging
import asyncio

class NotificationHandler:
    def __init__(self, bot):
        # Initialize the bot
        self.bot = bot

    
    async def send_welcome_message(self, chat_id):
        # Centralized method to send the welcome message
        await self.bot.send_message(chat_id=chat_id, text="Welcome to the bot!")

        
    async def send_already_registered_message(self, chat_id):
        # Centralized method to send the welcome message
        await self.bot.send_message(chat_id=chat_id, text="You are already registered chill!!")

    async def notify_users(self, transactions):
        # Get all users from the database
        users = get_all_users()

        for user in users:
            for tx in transactions:
                message = (
                    f"New transaction:\n\n"
                    f"Transaction date: {tx.transaction_date}\n"
                    f"Filind date: {tx.filing_date}\n"
                    f"Reporting Name: {tx.reporting_name}\n"
                    f"Activity: {tx.activity}\n"
                    f"Security: {tx.security}\n"
                    f"Shares: {tx.shares}\n"
                    f"Price: {tx.price}\n"
                    f"Total: {tx.total}"
                )
                try:
                    await self.bot.send_message(chat_id=user.chat_id, text=message)
                except Exception as e:
                    # Log any exception that occurs
                    logging.error(f"Failed to send message to {user.chat_id}: {e}")

                # Add a delay between each message to avoid hitting rate limits
                await asyncio.sleep(1)