import json
import re
from datetime import datetime, timedelta
from typing import Dict, List
import requests
from telebot import types
from loguru import logger
from loader import bot, LOCATION_URL, PROPERTIES_URL, PHOTO_URL, HEADERS


class ApiHandler:
    """Класс ApiHandler - выполняет все необходимые запросы к API и возвращает полученные данные.

    Attribute:
        locale (str): определяет, в какой зоне проводить поиск
    """
    locale = None

    @classmethod
    def find_city(cls, city: str, user_id: int) -> Dict[int, str]:
        """
        Метод класса город, в котором искать отели, передаёт все необходимые
        данные для поиска в API и получает найденный результат.

        :param city: город
        :param user_id: ID пользователя
        :return: словарь найденных ID городов
        :rtype: dict
        :raise ConnectionError: ошибка соединения с сервером
        """
        logger.info(f'Class {cls.__name__}: Function {cls.find_city.__name__.upper()} started.')

        template = r'[А-Яа-я]'
        locale = re.search(template, city)
        if locale:
            cls.locale = 'ru_RU'
            user_request = {'query': city, 'locale': 'ru_RU'}
        else:
            cls.locale = 'en_US'
            user_request = {'query': city, 'locale': 'en_US'}
        location_response = None
        result = None

        try:
            location_response = requests.get(url=LOCATION_URL, headers=HEADERS, params=user_request, timeout=10)
            if location_response.status_code != 200:
                result = json.loads(location_response.text)
                raise ConnectionError

            result = json.loads(location_response.text)
            find_city_id = searching_city_id(result)

        except ConnectionError:
            logger.error(f'Response status {location_response.status_code}: {result["message"]}.')
            bot.send_message(chat_id=user_id, text='Ошибка соединения с сервером, попробуйте позже.')
            raise

        except Exception as error:
            logger.error(f'{error}')
            bot.send_message(chat_id=user_id, text='Ошибка соединения с сервером, попробуйте позже.')
            raise

        else:
            logger.info(f'Class {cls.__name__}: Function {cls.find_city.__name__.upper()} completed.')
            return find_city_id

    @classmethod
    def find_hotel(cls, user_id: int, destination_id: int, amount_hotels_to_find: int,
                   command: str, price: list = None) -> List[Dict]:
        """
        Метод класса город. Ищет отели и передаёт все необходимые данные для поиска в API, получает найденный результат.

        :param user_id: ID пользователя
        :param destination_id: ID города
        :param amount_hotels_to_find: количество отелей для поиска
        :param command: команда, которую инициализировал пользователь
        :param price: ценовая категория, используется только при команде 'bestdeal'
        :return: список словарей найденных отелей и все необходимые параметры отелей
        :rtype: list[dict]
        """
        logger.info(f'Class {cls.__name__}: Function {cls.find_city.__name__.upper()} started.')

        check_in = datetime.now().strftime('%Y-%m-%d')
        check_out = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        if command == '/highprice':
            properties_request = {"destinationId": {destination_id}, "pageNumber": "1",
                                  "pageSize": {amount_hotels_to_find},
                                  f"checkIn": {check_in}, "checkOut": {check_out}, "adults1": "1",
                                  "sortOrder": 'PRICE_HIGHEST_FIRST', "locale": cls.locale, "currency": "RUB"}

        elif command == '/bestdeal':
            properties_request = {"destinationId": {destination_id}, "pageNumber": "1",
                                  "pageSize": {amount_hotels_to_find}, "checkIn": {check_in}, "checkOut": {check_out},
                                  "adults1": "1", "sortOrder": 'DISTANCE_FROM_LANDMARK', "locale": cls.locale,
                                  "currency": "RUB", 'priceMin': price[0], 'priceMax': price[1]}
        else:
            properties_request = {"destinationId": {destination_id}, "pageNumber": "1",
                                  "pageSize": {amount_hotels_to_find},
                                  f"checkIn": {check_in}, "checkOut": {check_out}, "adults1": "1",
                                  "sortOrder": 'PRICE', "locale": cls.locale, "currency": "RUB"}
        properties_response = None
        result = None

        try:
            properties_response = requests.request(method="GET", url=PROPERTIES_URL, headers=HEADERS,
                                                   params=properties_request, timeout=10)
            if properties_response.status_code != 200:
                result = json.loads(properties_response.text)
                raise ConnectionError

            result = json.loads(properties_response.text)

            find_properties = searching_hotels(result)

        except ConnectionError:
            logger.error(f'Response status {properties_response.status_code}: {result["message"]}')
            bot.send_message(chat_id=user_id, text='Ошибка соединения с сервером, попробуйте позже.')
            raise

        except Exception as error:
            logger.error(f'{error}')
            bot.send_message(chat_id=user_id, text='Ошибка соединения с сервером, попробуйте позже.')
            raise

        else:
            logger.info(f'Class {cls.__name__}: Function {cls.find_hotel.__name__.upper()} completed.')
            return find_properties

    @classmethod
    def find_photo(cls, user_id: int, hotels_id: list, how_many_pictures: int) -> List[List[types.InputMediaPhoto]]:
        """
        Метод класса получает список ID отелей для поиска фотографий для каждого отеля в списке.
        Использует API для получения фотографий.

        :param user_id: ID пользователя
        :param hotels_id: IDs отелей
        :param how_many_pictures: количество фотографий, которые надо найти для каждого отеля
        :return: список найденных фото, подготовленных к отправке в телеграм
        :rtype: list[list[types.InputMediaPhoto]]
        """
        logger.info(f'Class {cls.__name__}: Function {cls.find_photo.__name__.upper()} started.')

        photo_response = None
        result = None
        data = []

        try:
            for i_hotel_id in hotels_id:
                photo_request = {"id": i_hotel_id}
                photo_response = requests.request(method="GET", url=PHOTO_URL, headers=HEADERS, params=photo_request)

                if photo_response.status_code != 200:
                    result = json.loads(photo_response.text)
                    raise ConnectionError

                result = json.loads(photo_response.text)
                found_photos = searching_photo(result, hotels_id, how_many_pictures)
                data.append(found_photos)

        except ConnectionError:
            logger.error(f'Response status {photo_response.status_code}: {result["message"]}')
            bot.send_message(chat_id=user_id, text='Ошибка соединения с сервером, не получилось загрузить фотографии.')

        except Exception as error:
            logger.error(f'{error}')
            bot.send_message(chat_id=user_id, text='Ошибка соединения с сервером, не получилось загрузить фотографии.')

        else:
            logger.info(f'Class {cls.__name__}: Function {cls.find_photo.__name__.upper()} completed.')
            return data


def searching_city_id(api_dict: dict) -> Dict[int, str]:
    """
    Функция получает словарь от API, чтобы обработать и получить ID найденных городов.
    Например, пользователь ввёл в поиск "Москва" и было найдено 3 разных города Москва в мире.
    Эти ID сохраняются для дальнейшей обработки.

    :param api_dict: полученный словарь от API
    :return: словарь с найденными данными
    :rtype: dict[int, str]
    """
    logger.info(f'{searching_city_id.__name__.upper()} func started.')

    found_ids = {}

    try:
        for i_item in api_dict['suggestions']:
            if i_item['group'] == 'CITY_GROUP':
                for i_data in i_item.get('entities'):
                    template = re.sub(r'<.+?>', '', i_data['caption']).split(', ')
                    template = f'{template[0]}, {template[-1]}'
                    found_ids[int(i_data.get('destinationId'))] = f'{template}'

    except Exception as exception:
        logger.error(f'{exception}.')

    else:
        logger.info(f'{searching_city_id.__name__.upper()} func completed.')
        return found_ids


def searching_hotels(dict_of_properties: dict) -> List[dict]:
    """
    Функция получает словарь от API, чтобы обработать и получить все необходимые данные для отеля.
    ID, имя, рейтинг, адрес, город, страна, индекс, дистанция от центра города и цена за ночь.

    :param dict_of_properties: полученный словарь от API
    :return: список словарей для найденных данных
    :rtype: list[dict]
    """
    logger.info(f'{searching_hotels.__name__.upper()} func started.')

    hotels_requested = []
    try:
        for i_item in dict_of_properties['data'].get('body').get('searchResults').get('results'):
            dict_id = dict()
            dict_id['id'] = i_item.get('id')
            dict_id['name'] = i_item.get('name')
            dict_id['starRating'] = i_item.get('starRating')
            dict_id['address'] = i_item.get('address').get('streetAddress')
            dict_id['locality'] = i_item.get('address').get('locality')
            dict_id['postalCode'] = i_item.get('address').get('postalCode')
            dict_id['countryName'] = i_item.get('address').get('countryName')
            dict_id['distance'] = i_item.get('landmarks')[0].get('distance')
            dict_id['price'] = i_item.get('ratePlan').get('price').get('current')
            hotels_requested.append(dict_id)
    except KeyError as exception:
        logger.error(f'Key {exception} was not found.')

    logger.info(f'{searching_hotels.__name__.upper()} func completed.')
    return hotels_requested


def searching_photo(photos: dict, hotels_id: list, how_many_pictures: int) -> \
        List[types.InputMediaPhoto]:
    """
    Функция получает словарь от API, чтобы обработать и получить фотографии.

    :param photos: полученный список словарей от API
    :param hotels_id: ID отелей, к которым ищем фотографии
    :param how_many_pictures: количество фотографий необходимых найти для каждого отеля
    :return: список найденных фото, подготовленных к отправке в телеграм
    :rtype: list[types.InputMediaPhoto]
    """
    logger.info(f'{searching_photo.__name__.upper()} func started.')

    pictures_found = []

    for i_hotel in photos.values():
        pics_count = 0
        if i_hotel in hotels_id:
            while pics_count != how_many_pictures:
                pictures_found.append(
                    types.InputMediaPhoto(
                        photos['hotelImages'][pics_count]['baseUrl'].format(size='l')))
                pics_count += 1

    logger.info(f'{searching_photo.__name__.upper()} func completed.')
    return pictures_found
