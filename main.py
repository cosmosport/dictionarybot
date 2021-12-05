#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the GPLv3.0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import subprocess
import voice

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from my_dictionary import translate_words


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


# Ответ на сообщения, не являющиеся командами.
def reply(update: Update, context: CallbackContext) -> None:
    """
    Отправляет пользователю перевод слов из принятого сообщения,
    а также текст принятого сообщения, озвученный роботом.
    """
    update.message.reply_text(translate_words(update.message.text))
    audio_file_mp3 = voice.text_to_file(update.message.text)
    ogg_file_name = "reply_audio"
    audio_file_ogg = f"data/{ogg_file_name}.ogg"
    subprocess.run(["ffmpeg.exe", '-i', audio_file_mp3, '-acodec', 'libopus', audio_file_ogg, '-y'])
    update.message.reply_voice(voice=open(audio_file_mp3, "rb"))


def token():
    """
    Return the Telegram bot's token.
    Input the token from the command line if the file contains one is missing.
    """
    token_file_name = "TOKEN.txt"
    #token_file_name = "TKN.txt"
    try:
        token_file = open(token_file_name, "rt")
        token = token_file.readline()
        token_file.close()    
    except FileNotFoundError:
        token = input("Пожалуйста, введите токен, полученный при регистрации Telegram бота?\n")
        token_file = open(token_file_name, "wt")
        token_file.write(token)
        token_file.close()
    return token


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(token())

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - translate words of the message and send it back
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
