import db_handler
from loader import bot, user_info
from loguru import logger
from telebot import types
from user import User
from rapidapi import ApiHandler
import message_handlers.bestdeal as bestdeal
from telebot.apihelper import ApiTelegramException
from time import sleep


@logger.catch
def create_user(message: types.Message) -> None:
    """
    Функция создания экземпляра пользователя и его параметров.
    Запрашиваем, в каком городе нужно искать отели.

    :param message: выбранная команда пользователем
    :type message: types.Message
    """

    logger.info(f'Function {create_user.__name__.upper()} started. Command: {message.text}')
    user_info[message.chat.id] = User()
    user_info[message.chat.id].status = User.user_state[0]
    user_info[message.chat.id].first_name = message.chat.first_name
    user_info[message.chat.id].last_name = message.chat.last_name
    user_info[message.chat.id].user_id = message.chat.id
    user_info[message.chat.id].command = message.text
    user_info[message.chat.id].request_time = user_info[message.chat.id].time_converter(message.date)
    bot.send_message(message.chat.id, 'В каком городе нужен отель?')
    bot.register_next_step_handler(message, get_city)
    logger.info(f'Created new user: {message.chat.first_name} {message.chat.last_name}')


@logger.catch
def get_city(message: types.Message) -> None:
    """
    Функция поиска отелей. Сначала регистрируем, в каком городе искать, после обращаемся к класс ApiHandler
    и получаем от него словарь найденных отелей и выводим клавиатурой на экран для выбора одного варианта.

    :param message: город, в котором ищем отели
    :type message: types.Message
    """
    logger.info(f'Function {get_city.__name__.upper()} started.')

    bot.send_message(message.chat.id, text='Ищу нужный город.')
    user_info[message.chat.id].status = User.user_state[1]
    user_info[message.chat.id].city = message.text
    city_ids = ApiHandler.find_city(message.text, user_info[message.chat.id].user_id)

    max_offers = 8
    try:
        if len(city_ids.keys()) > 1:
            markup_inline = types.InlineKeyboardMarkup()
            all_data = []

            for i_key, i_val in city_ids.items():
                item = types.InlineKeyboardButton(text=str(i_val), callback_data=str('{} {}'.format(i_key, i_val)))
                all_data.append(markup_inline.add(item))
                if len(all_data) == max_offers:
                    break

            logger.info(f'Function {get_city.__name__.upper()} completed.')
            bot.send_message(message.chat.id, text='Выберите один из найденных вариантов:', reply_markup=markup_inline)
    except Exception as error:
        logger.error(f'Error: {error}.')
        bot.send_message(chat_id=message.chat.id, text='Ошибка ответа сервера. Попробуйте ввести данные латиницей.')
        raise

    if not len(city_ids.keys()):
        logger.error(f'City was not found. Function {create_user.__name__.upper()} will be re-started.')
        bot.send_message(chat_id=message.chat.id, text='Такой город либо не существует, либо не найден, попробуйте '
                                                       'ввести другой город.')
        create_user(message)


@logger.catch
def hotel_to_find(message: types.Message) -> None:
    """
    Функция регистрирующая какой точно город искать из предложенного списка,
    а также спрашивает, сколько всего отелей искать.

    :param message: Выбранный город из предложенного найденного списка
    :type message: types.Message
    """
    logger.info(f'Function {hotel_to_find.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[2]

    if user_info[message.chat.id].command == '/bestdeal':
        bot.send_message(message.chat.id, text='Сколько отелей искать?\nМаксимум 10.')
        bot.register_next_step_handler(message, bestdeal.price_range)
        logger.info(f'Function {hotel_to_find.__name__.upper()} completed.')

    else:
        bot.send_message(message.chat.id, text='Сколько отелей искать?\nМаксимум 10.')
        bot.register_next_step_handler(message, get_hotel)
        logger.info(f'Function {hotel_to_find.__name__.upper()} completed.')


@logger.catch
def get_hotel(message: types.Message) -> None:
    """
    Функция получает список словарей найденных отелей по заданным параметрам от пользователя.
    Узнаём у пользователя будет ли смотреть фотографии.

    :param message: объект сообщения пользователя
    :type message: types.Message
    """
    logger.info(f'Function {get_hotel.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[5]

    if user_info[message.chat.id].command == '/bestdeal':
        found_hotels = ApiHandler.find_hotel(
            user_id=user_info[message.chat.id].user_id,
            destination_id=user_info[message.chat.id].city_id,
            amount_hotels_to_find=user_info[message.chat.id].num_hotel,
            command=user_info[message.chat.id].command,
            price=user_info[message.chat.id].price)

    else:
        try:
            user_info[message.chat.id].num_hotel = int(message.text)
        except ValueError as ex:
            bot.send_message(chat_id=message.chat.id, text='Вы ввели не корректные данные. Введите число.')
            logger.error(f'User sent incorrect data and returning to the previous step. '
                         f'Error: {ex}')
            hotel_to_find(message)
            raise ValueError

        except Exception as error:
            logger.error(f'Additional error occurred: {error}')

        found_hotels = ApiHandler.find_hotel(
            user_id=user_info[message.chat.id].user_id,
            destination_id=user_info[message.chat.id].city_id,
            amount_hotels_to_find=user_info[message.chat.id].num_hotel,
            command=user_info[message.chat.id].command)

    user_info[message.chat.id].hotels = found_hotels

    for i_id in found_hotels:
        if not len(user_info[message.chat.id].hotels_id) == user_info[message.chat.id].num_hotel:
            hotel_id = i_id.get('id')
            user_info[message.chat.id].hotels_id.append(hotel_id)
            user_info[message.chat.id].hotel_url.append(f'https://ru.hotels.com/ho{hotel_id}')

    logger.info(f'Function {get_hotel.__name__.upper()} completed.')
    looking_for_photos(message)


@logger.catch
def looking_for_photos(message: types.Message) -> None:
    """Функция спрашивает у пользователя будет ли он смотреть фотографии.
    Выбор ответа через клавиатуру, либо да, либо нет.

    :param message: запрашиваем у пользователя данные
    :type message: types.Message
    """

    logger.info(f'Function {looking_for_photos.__name__.upper()} started.')
    user_info[message.chat.id].status = User.user_state[6]

    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Да!', callback_data='Да!')
    item_no = types.InlineKeyboardButton(text='Нет...', callback_data='Нет...')
    markup_inline.add(item_yes, item_no)
    bot.send_message(chat_id=message.chat.id, text='Будем смотреть фото?', reply_markup=markup_inline)
    logger.info(f'Function {looking_for_photos.__name__.upper()} completed.')


@logger.catch
def photo_to_find(message: types.Message) -> None:
    """
    Функция получает данные, что человек хочет посмотреть фото отелей и спрашивает, сколько фото для каждого отеля.

    :param message: получаем согласие пользователя на просмотр фотографий
    :type message: types.Message
    """
    logger.info(f'Function {photo_to_find.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[7]

    bot.send_message(message.chat.id, text='Сколько фотографий ищем?\nМаксимум 5.')
    bot.register_next_step_handler(message, get_photo)

    logger.info(f'Function {photo_to_find.__name__.upper()} completed.')


@logger.catch
def get_photo(message: types.Message) -> None:
    """
    Функция получает данные, сколько фотографий необходимо найти для каждого отеля.
    Обращается к классу ApiHandler и получает список найденных фотографий.

    :param message: данные, сколько человек хочет посмотреть фото для каждого отеля
    :type message: types.Message
    """
    logger.info(f'Function {get_photo.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[8]
    try:
        how_many_pictures = int(message.text)
    except ValueError as ex:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели не верные данные. Введите число.')
        logger.error(f'User sent incorrect data and returning to the previous step. '
                     f'Error: {ex}')
        raise ValueError

    user_info[message.chat.id].pics_to_find = how_many_pictures
    found_photos = ApiHandler.find_photo(
        user_id=user_info[message.chat.id].user_id,
        hotels_id=user_info[message.chat.id].hotels_id,
        how_many_pictures=how_many_pictures)
    user_info[message.chat.id].photos = found_photos

    if found_photos is None:
        bot.send_message(chat_id=message.chat.id, text='К сожалению, не смогли получить фотографии.')

    logger.info(f'Function {get_photo.__name__.upper()} completed.')
    printing_information(message)


@logger.catch
def printing_information(message: types.Message) -> None:
    """
    Функция собирает все необходимые данные и выводит на экран пользователю.

    :param message: объект сообщения пользователя
    :type message: types.Message
    """
    logger.info(f'Function {printing_information.__name__.upper()} started.')

    user_info[message.chat.id].status = User.user_state[9]

    if user_info[message.chat.id].command == '/bestdeal':
        db_handler.create_new_row_with_bestdeal(message.chat.id)
    else:
        db_handler.create_new_row_in_db(message.chat.id)

    try:
        if user_info[message.chat.id].photos is not None:
            for i_index, i_data in enumerate(user_info[message.chat.id].hotels):
                if i_index == user_info[message.chat.id].num_hotel:
                    break
                else:
                    sleep(0.5)
                    bot.send_media_group(message.chat.id, user_info[message.chat.id].photos[i_index])
                    bot.send_message(message.chat.id, 'Отель «{hotel_name}», рейтинг {rating}\n'
                                                      '{address}, {locality}\n{postalcode} {country}\n'
                                                      'Дистанция до центра города составляет {distance}.\n'
                                                      'Цена в отеле составляет {price}\n{url}'.format(
                                                        hotel_name=i_data['name'],
                                                        rating=i_data['starRating'],
                                                        address=i_data['address'],
                                                        locality=i_data['locality'],
                                                        postalcode=i_data['postalCode'],
                                                        country=i_data['countryName'],
                                                        distance=i_data['distance'],
                                                        price=i_data['price'],
                                                        url=user_info[message.chat.id].hotel_url[i_index]))
            logger.info(f'Function {printing_information.__name__.upper()} completed.')
        else:
            for i_index, i_data in enumerate(user_info[message.chat.id].hotels):
                if i_index == user_info[message.chat.id].num_hotel:
                    break
                else:
                    sleep(0.5)
                    bot.send_message(message.chat.id, 'Отель «{hotel_name}», рейтинг {rating}\n'
                                                      '{address}, {locality}\n{postalcode} {country}\n'
                                                      'Дистанция до центра города составляет {distance}.\n'
                                                      'Цена в отеле составляет {price}\n{url}'.format(
                                                        hotel_name=i_data['name'],
                                                        rating=i_data['starRating'],
                                                        address=i_data['address'],
                                                        locality=i_data['locality'],
                                                        postalcode=i_data['postalCode'],
                                                        country=i_data['countryName'],
                                                        distance=i_data['distance'],
                                                        price=i_data['price'],
                                                        url=user_info[message.chat.id].hotel_url[i_index]))
            logger.info(f'Function {printing_information.__name__.upper()} completed.')

    except ApiTelegramException as exception:
        logger.error(f'Error: {exception}')
    except Exception as error:
        logger.error(f'Additional error occurred: {error}')

    finally:
        logger.success(f'User {user_info[message.chat.id].first_name} {user_info[message.chat.id].last_name} '
                       f'successfully got all requested data.')
