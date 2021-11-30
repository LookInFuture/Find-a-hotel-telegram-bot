from peewee import Model, SqliteDatabase, IntegerField, CharField, FloatField, TextField, DateTimeField

database = SqliteDatabase('request_history.db')


class RequestHistory(Model):
    """
    Класс для создания БД. Родительский класс Model.

    user_id (int): ID пользователя
    name (str): Имя и фамилия пользователя
    city (str): Город, который ищем
    city_id (int): ID города
    price_min (float): минимальный диапазон цены
    price_max (float): максимальный диапазон цены
    distance_min (int): минимальный диапазон расстояния до центра города
    distance_max (int): максимальный диапазон расстояния до центра города
    num_hotel (int): количество отелей для поиска
    hotels (list[dict]): количество отелей для поиска
    request_time (datetime): время инициации запроса
    command (str): выбранная пользователем команда
    hotel_url (list[str]): ссылки на найденные отели
    """

    user_id = IntegerField()
    name = CharField()
    city = CharField()
    city_id = IntegerField()
    price_min = FloatField()
    price_max = FloatField()
    distance_min = IntegerField()
    distance_max = IntegerField()
    num_hotel = IntegerField()
    hotels = TextField()
    hotels_id = TextField()
    request_time = DateTimeField()
    command = CharField()
    hotel_url = TextField()

    class Meta:
        """
        Класс Meta. Содержит осноные настройки для БД.

        :param database (SqliteDatabase): класс будет использовать указанную ссылку на БД и работать с этой БД
        :param table_name (str): название таблицы
        :param order_by (str): сортирует по указанному значению
        """
        database = database
        table_name = 'request_history'
        order_by = 'request_time'


with database:
    RequestHistory.create_table()

