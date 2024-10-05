from stock_bot.handlers import get_all_users  # Import the function from handlers

class NotificationHandler:
    def __init__(self, bot):
        # Initialize the bot
        self.bot = bot

    
    def send_welcome_message(self, chat_id):
        # Centralized method to send the welcome message
        self.bot.send_message(chat_id=chat_id, text="Welcome to the bot!")

    def notify_users(self, transactions):
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
                # Send message to each user
                self.bot.send_message(chat_id=user.chat_id, text=message)
