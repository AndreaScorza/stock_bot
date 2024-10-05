from stock_bot.models import User, Transaction
from stock_bot.db import SessionLocal
import logging


def handle_new_user(chat_id, username):
    # Get a new session
    session = SessionLocal()

    # Check if the user already exists
    user = session.query(User).filter(User.chat_id == chat_id).first()

    if not user:
        # Add the user to the database
        new_user = User(chat_id=chat_id, username=username)
        session.add(new_user)
        session.commit()
        logging.info(f"Added new user: {username} ({chat_id})")
        session.close()
        return True  # New user added
    else:
        logging.info(f"User {username} ({chat_id}) already exists")
        session.close()
        return False  # User already exists


def store_new_transactions(transactions: list[Transaction]):
    session = SessionLocal()
    new_transactions = []

    for tx in transactions:
        # Eagerly load all required fields before the session is closed
        existing_tx = session.query(Transaction).filter_by(
            transaction_date=tx.transaction_date,
            reporting_name=tx.reporting_name,
            security=tx.security,
            activity=tx.activity,
            shares=tx.shares,
            price=tx.price,
            total=tx.total
        ).first()

        if not existing_tx:
            # Ensure we eagerly load all data before the session closes
            session.add(tx)
            new_transactions.append(tx)

    if new_transactions:
        session.commit()

    # Explicitly load the attributes before the session is closed
    for tx in new_transactions:
        session.refresh(tx)  # This ensures that all data is eagerly loaded
    
    session.close()
    return new_transactions

def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users

def delete_all_transactions():
    session = SessionLocal()

    try:
        # Delete all records from the Transaction table
        session.query(Transaction).delete()
        session.commit()
        print("All transactions have been deleted.")
    except Exception as e:
        session.rollback()  # Rollback in case of an error
        print(f"Error deleting transactions: {e}")
    finally:
        session.close()

def remove_last_transaction():
    session = SessionLocal()

    try:
        # Find the last inserted transaction (assuming an auto-incrementing primary key 'id')
        last_transaction = session.query(Transaction).order_by(Transaction.id.desc()).first()

        if last_transaction:
            session.delete(last_transaction)
            session.commit()
            logging.info(f"Deleted last transaction: {last_transaction}")
        else:
            logging.info("No transactions found to delete.")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error deleting the last transaction: {e}")
    
    finally:
        session.close()
