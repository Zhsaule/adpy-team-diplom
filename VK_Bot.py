import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Token import TOKEN #токен группы вк
from vkinder import VKinder_get_info, VKinder_get_photo


def write_msg(user_id, message, vk_session=vk_api.VkApi(token=TOKEN)):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})

favorites = []
user_info = []
def run_bot():
    global vk_inf, message
    vk_session = vk_api.VkApi(token=TOKEN)
    session_api = vk_session.get_api()
    longpool = VkLongPoll(vk_session)
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if str(message) == 'старт':
                    write_msg(event.user_id, f'Введите город, возраст,'
                    f' пол(м или ж) через запятую или пробел:')
                if len(message.split(',')) == 1:
                    message = ",".join(message.split(" "))
                if len(message.split(',')) != 3 and message != 'старт' and message != 'нравится':
                    write_msg(event.user_id, 'Введены некорректные данные')
                elif len(message.split(',')) == 3:
                    response = message.split(",")
                    city, age, sex = response
                    vk_inf = VKinder_get_info(str(sex), int(age), city.title())
                    if len(vk_inf.get_inf()) != 0:
                        write_msg(event.user_id, f'{vk_inf.get_inf()[0][0]} {vk_inf.get_inf()[0][1]} - {vk_inf.get_inf()[0][3]}')
                        if [f"{event.user_id}, {sex}, {age}, {city}"] not in user_info:
                            user_info.append([f"{event.user_id}, {sex}, {age}, {city}"])
                        if VKinder_get_photo(vk_inf.get_inf()[0][2]).get_photo_url() is not None:
                            for i in VKinder_get_photo(vk_inf.get_inf()[0][2]).get_photo_url():
                                time.sleep(0.2)
                                write_msg(event.user_id, i)
                print(user_info)
                if message == 'нравится':
                    favorites.append([event.user_id, *vk_inf.get_inf()])
                    print(favorites)
                elif message == 'стоп':
                    break
