from loader import bot, user_info
from loguru import logger
from telebot import types
from message_handlers.message_handlers import create_user, get_city, photo_to_find, printing_information, \
    hotel_to_find, get_photo, looking_for_photos
from message_handlers.bestdeal import price_range, distances
from db_handler import get_data_from_db

commands = ['start', 'lowprice', 'highprice', 'bestdeal', 'history', 'help']


@bot.message_handler(commands=commands)
def bot_commands(message: types.Message) -> None:
    """
    Функция обрабатывающая доступные команды пользователя.

    :param message: полученная команда от пользователя
    """
    logger.info(f'User has sent message: {message.text}.')
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         'Добро пожаловать, {0.first_name} {0.last_name}!\nЯ - {1.first_name} бот созданный чтобы '
                         'помочь тебе найти подходящий отель!\nЖми /help, чтобы получить актуальные команды!'.format(
                             message.from_user, bot.get_me()))
    elif message.text == '/lowprice':
        create_user(message)
    elif message.text == '/highprice':
        create_user(message)
    elif message.text == '/bestdeal':
        create_user(message)
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'Вот список доступных команд:\n'
                                          '/lowprice — поиск отелей по самой дешёвой цене.\n'
                                          '/highprice — поиск отелей по самой дорогой цене.\n'
                                          '/bestdeal — лучшее предложение. Здесь доступны сортировка цены '
                                          'по диапазону, сортировка удалённости от центра.\n'
                                          '/history — история запросов.')
    elif message.text == '/history':
        get_data_from_db(message.chat.id)


@bot.message_handler(content_types='text')
def hello_world(message: types.Message) -> None:
    """
    Функция обрабатывающая приветсвие пользователя.

    :param message: приветствие от пользователя
    """
    logger.info(f'User has sent message: {message.text}.')

    if message.text.lower().startswith('привет'):
        bot.send_message(message.chat.id, 'Привет, {}! Готов к путешествиям?'.format(message.chat.first_name))
        bot.send_message(message.chat.id, 'Жми /help и погнали! 🚀')

    else:
        check_status(message.chat.id)


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: types.CallbackQuery) -> None:
    """
    Функция обработки нажатия кнопок пользователем

    :param call: объект входящего сообщения от пользователя
    :type call: types.CallbackQuery
    """
    logger.info(f'Function {callback_handler.__name__.upper()} started.')
    logger.info(f'User response: {call.data}')

    if call.data == 'Да!':
        logger.info(f'Function {callback_handler.__name__.upper()} completed.')
        photo_to_find(call.message)

    elif call.data == 'Нет...':
        bot.send_message(call.message.chat.id, text='Хорошо!')
        bot.send_message(call.message.chat.id, text='Выводим информацию.')
        logger.info(f'Function {callback_handler.__name__.upper()} completed.')
        printing_information(call.message)

    elif call.data == 'continue':
        try:
            user_status = user_info[call.message.chat.id].status
            for i_status in user_status.keys():
                if i_status == 1:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    get_city(call.message)
                elif i_status == 2:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    hotel_to_find(call.message)
                elif i_status == 3:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    price_range(call.message)
                elif i_status == 4:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    distances(call.message)
                elif i_status == 5:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    hotel_to_find(call.message)
                elif i_status == 6:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    looking_for_photos(call.message)
                elif i_status == 7:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    photo_to_find(call.message)
                elif i_status == 8:
                    logger.info(f'Function {callback_handler.__name__.upper()} completed.')
                    get_photo(call.message)
                else:
                    logger.error(f'User has sent incorrect data. User has been sent to the beginning.')
                    bot.send_message(chat_id=call.message.chat.id,
                                     text='Нажмите /help, для получения актуальных команд.')

        except KeyError as key_error:
            logger.error(f'Key error, user {key_error} is not created yet. '
                         f'User has been sent to the beginning.')
            bot.send_message(chat_id=key_error, text='Вы что-то делаете не так. Нажмите /help, для получения '
                                                     'актуальных команд.')

    elif call.data == 'break':
        logger.info(f'Function {callback_handler.__name__.upper()} completed.')
        bot.send_message(chat_id=call.message.chat.id, text='Нажмите /help, для получения актуальных команд.')

    else:
        call_data = call.data.split()
        user_info[call.message.chat.id].city_id = call_data[0]
        user_info[call.message.chat.id].city = ' '.join(call_data[1:])
        logger.info(f'Function {callback_handler.__name__.upper()} completed.')
        hotel_to_find(call.message)


@logger.catch
def check_status(user_id: int) -> None:
    logger.info(f'Function {check_status.__name__.upper()} started.')

    bot.send_message(chat_id=user_id, text='Введённые данные не корректны.')
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Продолжить', callback_data='continue')
    item_no = types.InlineKeyboardButton(text='Начать заново', callback_data='break')
    markup_inline.add(item_yes, item_no)
    bot.send_message(chat_id=user_id, text='Хотите продолжить или начать заново?', reply_markup=markup_inline)
