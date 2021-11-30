from loader import bot, user_info
from user import User
import re
from telebot import types
from loguru import logger
import message_handlers.message_handlers


@logger.catch
def price_range(message: types.Message) -> None:
    """
    Функция регистрирующая сколько всего отелей искать. После чего узнаёт в каком ценовом диапазоне искать отели.
    Работает только с командой /bestdeal.

    :param message: количество отелей для поиска.
    :type message: types.Message
    """
    logger.info(f'Function {price_range.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[3]

    try:
        user_info[message.chat.id].num_hotel = int(message.text)
    except ValueError as ex:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели не верные данные. Введите число.')
        message_handlers.message_handlers.hotel_to_find(message)
        logger.error(f'User sent incorrect data and returning to the previous step. '
                     f'Error: {ex}')
        raise ValueError

    bot.send_message(message.chat.id, 'Какой ценовой диапазон?\nНапример: 100-200')
    bot.register_next_step_handler(message, search_price)

    logger.info(f'Function {price_range.__name__.upper()} completed')


@logger.catch
def search_price(message: types.Message) -> None:
    """
    Функция регистрирующая ценовой диапазон. Проверяет, что первое число введённое пользователем не больше второго,
    если выражение не верно, то ставит цены в правильной последовательности.
    После чего узнаёт на каком расстоянии отель должен находиться от центра города.
    Работает только с командой /bestdeal.

    :param message: ценовой диапазон
    :type message: types.Message
    """
    logger.info(f'Function {search_price.__name__.upper()} started.')

    template = re.search(r'\d+\s*?-?\s*?\d+', message.text)

    checking_data = message.text

    if checking_data.startswith('-') or checking_data.startswith('0'):
        logger.error(f'Wrong input data. Function {search_price.__name__.upper()} re-started.')
        bot.send_message(chat_id=message.chat.id, text='Введённые данные не корректны. Попробуйте снова.')
        bot.register_next_step_handler(message, search_price)
        return

    if template:
        try:
            price = message.text.split('-')
            if int(price[0]) > int(price[1]):
                price[0], price[1] = price[1], price[0]

        except ValueError as value_error:
            logger.error(f'Wrong input data: {value_error}.')
            price = message.text.split()
            if int(price[0]) > int(price[1]):
                price[0], price[1] = price[1], price[0]
            else:
                logger.error(f'Wrong input data. Function {search_price.__name__.upper()} re-started.')
                bot.send_message(chat_id=message.chat.id, text='Введённые данные не корректны. Попробуйте снова.')
                bot.register_next_step_handler(message, search_price)

        except IndexError as index_error:
            logger.error(f'Wrong input data: {index_error}.')
            bot.send_message(chat_id=message.chat.id, text='Введённые данные не корректны. Попробуйте снова.')
            bot.register_next_step_handler(message, search_price)
            raise IndexError

        user_info[message.chat.id].price = [int(price[0]), int(price[1])]
        bot.send_message(message.chat.id, 'На каком расстроянии должен находиться отель от центра города?\n'
                                          'Например: 1-5')
        bot.register_next_step_handler(message, distances)
        logger.info(f'Function {search_price.__name__.upper()} completed.')

    else:
        bot.send_message(message.chat.id, 'Введены не правильные данные. Попробуйте ещё раз.')
        bot.send_message(message.chat.id, 'Какой ценовой диапазон?\nНапример: 100-200')
        bot.register_next_step_handler(message, search_price)
        logger.error(f'Wrong input data. Function {search_price.__name__.upper()} re-started.')


@logger.catch
def distances(message: types.Message) -> None:
    """
    Функция регистрирующая диапазон расстояния от центра города. Проверяет, что первое число введённое пользователем
    не больше второго, если выражение не верно, то ставит цены в правильной последовательности.
    Работает только с командой /bestdeal.

    :param message: диапазон расстояния от центра города
    :type message: types.Message
    """
    logger.info(f'Function {distances.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[4]

    template = re.search(r'\d+\s*?-?\s*?\d+', message.text)

    checking_data = message.text

    if checking_data.startswith('-'):
        logger.error(f'Wrong input data. Function {search_price.__name__.upper()} re-started.')
        bot.send_message(chat_id=message.chat.id, text='Введённые данные не корректны. Попробуйте снова.')
        bot.register_next_step_handler(message, distances)
        return

    if template:
        try:
            distance = message.text.split('-')
            if int(distance[0]) > int(distance[1]):
                distance[0], distance[1] = distance[1], distance[0]

        except ValueError as value_error:
            logger.error(f'Wrong input data: {value_error}.')
            distance = message.text.split()
            if int(distance[0]) > int(distance[1]):
                distance[0], distance[1] = distance[1], distance[0]
            else:
                logger.error(f'Wrong input data. Function {distances.__name__.upper()} re-started.')
                bot.send_message(chat_id=message.chat.id, text='Введённые данные не корректны. Попробуйте снова.')
                bot.register_next_step_handler(message, distances)

        except IndexError as index_error:
            logger.error(f'Wrong input data: {index_error}.')
            bot.send_message(chat_id=message.chat.id, text='Введённые данные не корректны. Попробуйте снова.')
            bot.register_next_step_handler(message, distances)
            raise IndexError

        user_info[message.chat.id].distance = [int(distance[0]), int(distance[1])]

    else:
        bot.send_message(message.chat.id, 'Введены не правильные данные. Попробуйте ещё раз.')
        bot.register_next_step_handler(message, distances)
        logger.error(f'Wrong input data. Function {distances.__name__.upper()} re-started.')
        raise

    user_info[message.chat.id].distance = [int(distance[0]), int(distance[1])]

    logger.info(f'Function {distances.__name__.upper()} completed.')
    message_handlers.message_handlers.get_hotel(message)
