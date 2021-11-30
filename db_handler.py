from models import database
from models import RequestHistory
from loguru import logger
from loader import bot, user_info
from time import sleep


@logger.catch
def create_new_row_in_db(user_id: int) -> None:
    logger.info(f'Creating user {user_id} in DB.')
    with database:
        RequestHistory.create(user_id=user_id,
                              name=f'{user_info[user_id].first_name} {user_info[user_id].last_name}',
                              command=user_info[user_id].command,
                              request_time=user_info[user_id].request_time,
                              city=user_info[user_id].city,
                              city_id=user_info[user_id].city_id,
                              price_min='NULL',
                              price_max='NULL',
                              distance_min='NULL',
                              distance_max='NULL',
                              num_hotel=user_info[user_id].num_hotel,
                              hotels=user_info[user_id].hotels,
                              hotels_id=user_info[user_id].hotels_id,
                              hotel_url=user_info[user_id].hotel_url)


@logger.catch
def create_new_row_with_bestdeal(user_id: int) -> None:
    logger.info(f'Creating user {user_id} in DB.')
    with database:
        RequestHistory.create(user_id=user_id,
                              name=f'{user_info[user_id].first_name} {user_info[user_id].last_name}',
                              command=user_info[user_id].command,
                              request_time=user_info[user_id].request_time,
                              city=user_info[user_id].city,
                              city_id=user_info[user_id].city_id,
                              price_min=user_info[user_id].price[0],
                              price_max=user_info[user_id].price[1],
                              distance_min=user_info[user_id].distance[0],
                              distance_max=user_info[user_id].distance[1],
                              num_hotel=user_info[user_id].num_hotel,
                              hotels=user_info[user_id].hotels,
                              hotels_id=user_info[user_id].hotels_id,
                              hotel_url=user_info[user_id].hotel_url)


@logger.catch
def get_data_from_db(user_id: int) -> None:
    with database:
        hotels = RequestHistory.select().where(RequestHistory.user_id == user_id)
        urls_to_deliver = list()
        hotels_pulled_from_db = list()
        hotels_to_deliver = dict()

        bot.send_message(chat_id=user_id, text='История ваших запросов:')

        for i_hotels in hotels:
            urls_to_deliver.extend(eval(i_hotels.hotel_url))
            hotels_pulled_from_db.append(eval(i_hotels.hotels))

            bot.send_message(chat_id=user_id,
                             text=f'Время запроса: {i_hotels.request_time}\nИспользуемая команда: {i_hotels.command}\n'
                                  f'Вы искали: {i_hotels.city}.')

            for i_hotel in hotels_pulled_from_db:

                for i_data in i_hotel:
                    hotels_to_deliver[i_data['id']] = [i_data['name'], i_data['price']]

                hotels_pulled_from_db.pop(0)

                for i_data, i_val in hotels_to_deliver.items():
                    sleep(0.5)
                    bot.send_message(chat_id=user_id, text=f'Название отеля: {i_val[0]}\n'
                                                           f'Цена: {i_val[1]}\n'
                                                           f'Ссылка на отель: {urls_to_deliver[0]}')
                    urls_to_deliver.pop(0)

                hotels_to_deliver.clear()

        for person in RequestHistory.select().where(RequestHistory.user_id == user_id):
            logger.success(f'User {person.name} successfully got all history data.')
            return
