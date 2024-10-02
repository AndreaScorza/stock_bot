from sqlalchemy.orm import Session
from stock_bot.models import User
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
    else:
        print(f"User {username} ({chat_id}) already exists")

    session.close()
