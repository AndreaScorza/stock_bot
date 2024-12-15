### Consideration

The transaction is added to the db, before the notification is sent, there might be an error where the notification is not sent but the tx is added to the db, resulting in the user not seeing the notification.


---

Also since the polling and the await for the scraper cannot work together, instead of setting up a server listening to both webhooks to send notifications i've decided the easiest way would be to have two scripts, one polling for new users, and one scraping.
For sure in the future it will have to be updated with the both just waiting for triggers, and the telegram set on webhook and the scraping service sending a requests with a transaction when a new transatcion is found.


## Set up with systemd

new_user_bot.service

```
[Unit]
Description=New User Bot Service
After=network.target

[Service]
ExecStart=/bin/bash -c "poetry run python stock_bot/new_user.py"
Restart=always
User=pi
WorkingDirectory=/home/pi/github/stock_bot
Environment="PATH=/home/pi/.local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```
sudo systemctl start new_user_bot.service   # For stating it

sudo systemctl status new_user_bot.service  # For checking the logs

sudo systemctl enable new_user_bot.service  # For restarting it after a reboot


transaction_bot.service

```
[Unit]
Description=Transaction Bot Service
After=network.target

[Service]
ExecStart=/bin/bash -c "poetry run python stock_bot/bot.py"
WorkingDirectory=/home/pi/github/stock_bot
User=pi
Environment="PATH=/home/pi/.local/bin:/usr/bin:/bin"
```

transaction_bot.timer
```
[Unit]
Description=Run Transaction Bot Twice Daily

[Timer]
OnCalendar=*-*-* 10:00:00
OnCalendar=*-*-* 22:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

sudo systemctl enable transaction_bot.timer

sudo systemctl start transaction_bot.timer