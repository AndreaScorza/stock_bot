import pytest
from stock_bot.scraper import fetch_transactions
from stock_bot.models import Transaction

def test_fetch_transactions_integration():
    # Call the real function to fetch transactions
    transactions = fetch_transactions()

    # Assert the output is a list
    assert isinstance(transactions, list)

    # Assert the list contains Transaction objects
    assert len(transactions) > 0  # Ensure we got some transactions

    # Check that the first transaction is an instance of the Transaction class
    assert isinstance(transactions[0], Transaction)

    # Check that the fields of the first transaction match the expected format
    first_transaction = transactions[0]
    assert isinstance(first_transaction.transaction_date, str)
    assert isinstance(first_transaction.filing, str)
    assert isinstance(first_transaction.reporting_name, str)
    assert isinstance(first_transaction.activity, str)
    assert isinstance(first_transaction.security, str)
    assert isinstance(first_transaction.shares, str)
    assert isinstance(first_transaction.price, str)
    assert isinstance(first_transaction.total, str)
