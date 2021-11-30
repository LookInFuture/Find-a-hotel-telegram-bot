import os
import telebot
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
rapid_key = os.getenv('RAPID_KEY')

LOCATION_URL = "https://hotels4.p.rapidapi.com/locations/search"
PROPERTIES_URL = "https://hotels4.p.rapidapi.com/properties/list"
PHOTO_URL = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
HEADERS = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': rapid_key
}

logger.add('logger.log', format='{time: YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
           level='DEBUG', rotation='1 week', retention='1 week', encoding='UTF-8')

user_info = dict()