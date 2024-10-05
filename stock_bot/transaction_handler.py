from stock_bot.scraper import fetch_transactions
from stock_bot.handlers import store_new_transactions
import logging

class TransactionHandler:

    def fetch_and_store(self):
        logging.info("Running transaction fetching job...")

        # Fetch the latest transactions from the website
        transactions = fetch_transactions()

        # Store new transactions in the database and return the new transactions
        new_transactions = store_new_transactions(transactions)

        # Return the list of new transactions (empty if none)
        return new_transactions