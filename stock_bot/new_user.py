import logging
from telegram import Update
from telegram.ext import Application, CommandHandler
from stock_bot.config import Config
from stock_bot.db_handler import handle_new_user, delete_user
from stock_bot.notification_handler import NotificationHandler
from stock_bot.db import init_db

# Function to handle the /start command
async def handle_start_command(update: Update, context):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "Unknown"
    
    logging.info(f"Received /start command from user {username} (chat_id={chat_id})")

    # Add the user to the database if they're new
    is_new_user = handle_new_user(chat_id, username)
    
    # Notify the user based on whether they're new or existing
    notifier = NotificationHandler(context.bot)
    if is_new_user:
        logging.info(f"New user {username} added to the database.")
        await notifier.send_welcome_message(chat_id)
    else:
        logging.info(f"User {username} is already registered.")
        await notifier.send_already_registered_message(chat_id)


# Function to handle the /delete command
async def handle_delete_command(update: Update, context):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "Unknown"
    
    logging.info(f"Received /delete command from user {username} (chat_id={chat_id})")

    # Try to delete the user
    if delete_user(chat_id):
        await update.message.reply_text("You have been successfully removed from the bot's user list. "
                                      "You can always start again with /start command.")
    else:
        await update.message.reply_text("You are not registered with this bot.")


# Main class for managing the Telegram bot
class NewUserBot:
    def __init__(self):
        # Set up the bot
        self.application = Application.builder().token(Config.BOT_TOKEN).build()

    def run_polling(self):
        logging.info("Starting Telegram polling...")
        # Start polling for Telegram messages
        self.application.run_polling()

    def run(self):
        # Add command handlers
        start_handler = CommandHandler('start', handle_start_command)
        delete_handler = CommandHandler('delete', handle_delete_command)
        self.application.add_handler(start_handler)
        self.application.add_handler(delete_handler)

        logging.info("Initializing the bot...")
        self.application.initialize()

        logging.info("Starting polling...")
        self.run_polling()


# Entry point for running the new user bot independently
def main():
    # Initialize the database
    init_db()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create and run the bot
    bot = NewUserBot()
    bot.run()


if __name__ == "__main__":
    main()
