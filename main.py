from loader import bot
from loguru import logger
from commands_handler import bot_commands

if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception as exception:
            logger.critical(f'Unknown error: {exception}. Bot isn\'t running.')
