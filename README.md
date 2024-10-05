### Consideration

The transaction is added to the db, before the notification is sent, there might be an error where the notification is not sent but the tx is added to the db, resulting in the user not seeing the notification.


---

Also since the polling and the await for the scraper cannot work together, instead of setting up a server listening to both webhooks to send notifications i've decided the easiest way would be to have two scripts, one polling for new users, and one scraping.
For sure in the future it will have to be updated with the both just waiting for triggers, and the telegram set on webhook and the scraping service sending a requests with a transaction when a new transatcion is found.