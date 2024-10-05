#!/bin/bash

poetry run python stock_bot/new_user.py &
poetry run python stock_bot/bot.py &
wait