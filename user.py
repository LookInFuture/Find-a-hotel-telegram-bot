import datetime
from typing import List
from telebot import types


class User:
    """
    Класс User, который сохраняет все необходимые данные о запросах пользователя

    user_state (dict): отслеживает на каком шаге находится пользователь при взаимодействии с ботом

    Attributes:
        _first_name (str): имя пользователя
        _last_name (str): фамилия пользователя
        _user_id (int): ID пользователя
        _city (str): город, запрошенный пользователем
        _city_id (int): ID города, полученный через API
        _price (list[int]): диапазон цен, в котором нужно производить поиск отелей
        _distance (list[int]): диапазон расстояния, в котором нужно производить поиск отелей
        _num_hotel (int): количество отелей для поиска запрошенные пользователем
        _hotels (list[dict]): список найденных отелей
        _hotels_id (list[int]): список ID найденных отелей
        _photos (list[types.InputMediaPhoto): список найденных фотографий искомых отелей
        _pics_to_find (int): количество фоторафий, необходимых найти для каждого отеля
        _request_time (datetime): время инициализации работы пользователя с ботом
        _command (str): выбранная пользователем команда для выполнения
        _hotel_url (list[str]): список найденных ссылок для запрошенных отелей
        _status (dict[int, str]): список найденных ссылок для запрошенных отелей
    """

    user_state = [
        {0: 'Beginning step'},
        {1: 'Getting city'},
        {2: 'Searching hotel'},
        {3: 'Price range'},
        {4: 'Distance range'},
        {5: 'Getting hotel'},
        {6: 'Wish to see a photo?'},
        {7: 'How many photos?'},
        {8: 'Getting photos'},
        {9: 'Printing information'}
    ]

    def __init__(self):
        self._first_name = None
        self._last_name = None
        self._user_id = None
        self._city = None
        self._city_id = None
        self._price = []
        self._distance = []
        self._num_hotel = None
        self._hotels = None
        self._hotels_id = []
        self._photos = None
        self._pics_to_find = None
        self._request_time = None
        self._command = None
        self._hotel_url = []
        self._status = None

    @classmethod
    def time_converter(cls, time: datetime) -> datetime:
        """
        Функция конвертации времени, для последующего сохранения в БД в добном виде для админа.
        :param time: получает на вход текущее время
        :rtype: datetime.str
        """
        return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def first_name(self) -> str:
        """
        Геттер имени пользователя
        :rtype: str
        """
        return self._first_name

    @property
    def last_name(self) -> str:
        """
        Геттер фамилии пользователя
        :rtype: str
        """
        return self._last_name

    @property
    def user_id(self) -> int:
        """
        Геттер ID пользователя
        :rtype: int
        """
        return self._user_id

    @property
    def city(self) -> str:
        """
        Геттер искомого города
        :rtype: str
        """
        return self._city

    @property
    def city_id(self) -> str:
        """
        Геттер ID города
        :rtype: str
        """
        return self._city_id

    @property
    def price(self) -> List[int]:
        """
        Геттер списка диапазона цен, в котором должен происходить поиск отелей
        :rtype: list
        """
        return self._price

    @property
    def distance(self) -> List[int]:
        """
        Геттер списка диапазона расстояния от центра города, в котором должен происходить поиск отелей
        :rtype: list
        """
        return self._distance

    @property
    def num_hotel(self) -> int:
        """
        Геттер количества запрошенных пользователем отелей для поиска
        :rtype: int
        """
        return self._num_hotel

    @property
    def hotels(self) -> List[dict]:
        """
        Геттер списка найденных отелей
        :rtype: list
        """
        return self._hotels

    @property
    def hotels_id(self) -> List[int]:
        """
        Геттер списка найденных ID отелей
        :rtype: list
        """
        return self._hotels_id

    @property
    def photos(self) -> List[types.InputMediaPhoto]:
        """
        Геттер списка найденных фоторграфий для каждого отеля
        :rtype: list
        """
        return self._photos

    @property
    def pics_to_find(self) -> int:
        """
        Геттер количества запрошенных фотографий необходимых найти для каждого отеля
        :rtype: int
        """
        return self._pics_to_find

    @property
    def request_time(self) -> datetime:
        """
        Геттер получения времени, когда пользователь инициировал работу с ботом
        :rtype: datetime
        """
        return self._request_time

    @property
    def command(self) -> str:
        """
        Геттер получения команды, которую инициировал пользователь
        :rtype: str
        """
        return self._command

    @property
    def hotel_url(self) -> list:
        """
        Геттер получения списка ссылок найденных отелей
        :rtype: list
        """
        return self._hotel_url

    @property
    def status(self) -> dict:
        """
        Геттер получения на каком этапе находится пользователь
        :rtype: dict
        """
        return self._status

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        """
        Сеттер имени
        :param first_name: имя
        :type first_name: str
        """
        self._first_name = first_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        """
        Сеттер фамилии
        :param last_name: фамилия
        :type last_name: str
        """
        self._last_name = last_name

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """
        Сеттер ID пользователя
        :param user_id: ID
        :type user_id: int
        """
        self._user_id = user_id

    @city.setter
    def city(self, city: str) -> None:
        """
        Сеттер искомого города
        :param city: город
        :type city: str
        """
        self._city = city

    @city_id.setter
    def city_id(self, city_id: str) -> None:
        """
        Сеттер ID города
        :param city_id: ID города
        :type city_id: str
        """
        self._city_id = city_id

    @price.setter
    def price(self, price: List[int]) -> None:
        """
        Сеттер диапазона цен
        :param price: диапазон цен
        :type price: list
        """
        self._price = price

    @distance.setter
    def distance(self, distance: List[int]) -> None:
        """
        Сеттер диапазона расстояния
        :param distance: диапазон расстояния
        :type distance: list[int]
        """
        self._distance = distance

    @num_hotel.setter
    def num_hotel(self, num_hotel: int) -> None:
        """
        Сеттер количества отелей для поиска
        :param num_hotel: количество отелей для поиска
        :type num_hotel: int
        """
        self._num_hotel = num_hotel

    @hotels.setter
    def hotels(self, hotels: List[dict]) -> None:
        """
        Сеттер списка найденных отелей
        :param hotels: список найденных отелей
        :type hotels: list
        """
        self._hotels = hotels

    @hotels_id.setter
    def hotels_id(self, hotels_id: List[int]) -> None:
        """
        Сеттер списка ID найденных отелей
        :param hotels_id: список ID найденных отелей
        :type hotels_id: list
        """
        self._hotels_id = hotels_id

    @photos.setter
    def photos(self, photos: List[types.InputMediaPhoto]) -> None:
        """
        Сеттер списка найденных фотографий
        :param photos: список найденных фотографий
        :type photos: list
        """
        self._photos = photos

    @pics_to_find.setter
    def pics_to_find(self, pics_to_find: int) -> None:
        """
        Сеттер количества фотографий необходимых найти
        :param pics_to_find: количество фотографий необходимых найти
        :type pics_to_find: int
        """
        self._pics_to_find = pics_to_find

    @request_time.setter
    def request_time(self, request_time: datetime) -> None:
        """
        Сеттер установления времени, когда пользователь инициализировал команду бота
        :param request_time: время
        :type request_time: datetime
        """
        self._request_time = request_time

    @command.setter
    def command(self, command: str) -> None:
        """
        Сеттер какую команду выбрал пользователь
        :param command: команда боту
        :type command: str
        """
        self._command = command

    @hotel_url.setter
    def hotel_url(self, hotel_url: list) -> None:
        """
        Сеттер списка найденных ссылок отелей
        :param hotel_url: список ссылок отелей
        :type hotel_url: str
        """
        self._hotel_url = hotel_url

    @status.setter
    def status(self, status: dict) -> None:
        """
        Сеттер для установления на каком шаге находится пользователь.
        :param status: строка, описывающая статус пользователя.
        :type: status: dict
        """
        self._status = status



