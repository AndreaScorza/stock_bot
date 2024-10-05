### Consideration

The transaction is added to the db, before the notification is sent, there might be an error where the notification is not sent but the tx is added to the db, resulting in the user not seeing the notification.
