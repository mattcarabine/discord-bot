#!/usr/bin/env bash
python /discord-bot/util/setup_directory.py
python /discord-bot/util/import-champs.py
python /discord-bot/discord-bot/discord-bot.py