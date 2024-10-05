from stock_bot.models import User, Transaction
from stock_bot.db import SessionLocal


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
        print(f"Added new user: {username} ({chat_id})")
        session.close()
        return True  # New user added
    else:
        print(f"User {username} ({chat_id}) already exists")
        session.close()
        return False  # User already exists

def store_new_transactions(transactions):
        session = SessionLocal()
        new_transactions = []

        for tx in transactions:
            # Check if the transaction already exists in the database
            existing_tx = session.query(Transaction).filter_by(
                transaction_date=tx['transaction_date'],
                reporting_name=tx['reporting_name'],
                security=tx['security'],
                activity=tx['activity'],
                shares=tx['shares'],
                price=tx['price'],
                total=tx['total']
            ).first()

            if not existing_tx:
                # Add new transaction to the database
                new_tx = Transaction(**tx)
                session.add(new_tx)
                new_transactions.append(new_tx)

        if new_transactions:
            session.commit()

        session.close()
        return new_transactions


def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users
