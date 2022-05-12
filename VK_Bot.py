import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Token import GROUP_TOKEN  # токен группы вк
from vkinder import VKinder_get_info, VKinder_get_photo
from vkinder import MessagesSend


def write_msg(user_id, message, vk_session=vk_api.VkApi(token=GROUP_TOKEN)):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


favorites = []
user_info = []


def run_bot():
    global vk_inf, message
    vk_session = vk_api.VkApi(token=GROUP_TOKEN)
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
                    write_msg(event.user_id,
                              'Проверьте правильность набора. Введите: ваш город, ваш возраст, ваш пол(м или ж)')
                elif len(message.split(',')) == 3:
                    response = message.split(",")
                    response = [i.strip().title() for i in response]
                    city, age, sex = response
                    if age.isdigit() is True:
                        if int(age) < 16:
                            write_msg(event.user_id, "Возрастное ограничение 16+")
                        else:
                            info = VKinder_get_info(str(sex).lower(), int(age), str(city.title())).get_inf()
                            if info is None:
                                write_msg(event.user_id,
                                          'Проверьте правильность набора. Введите: ваш город, ваш возраст, ваш пол(м или ж)')
                            else:
                                if len(info) != 0:
                                    write_msg(event.user_id, f'{info[0]} {info[1]} - {info[3]}')
                                    if [f"{event.user_id}, {sex}, {age}, {city}"] not in user_info:
                                        user_info.append([f"{event.user_id}, {sex}, {age}, {city}"])
                                    photos = VKinder_get_photo(info[2]).get_photo_url()
                                    if photos is not None:
                                        for i in photos:
                                            MessagesSend(event.user_id, i).send_photo()
                                else:
                                    write_msg(event.user_id, "Не найдено совпадений. Попробуйте еще раз!")
                    else:
                        write_msg(event.user_id,
                                  'Проверьте правильность набора. Введите: ваш город, ваш возраст, ваш пол(м или ж)')
                print(user_info)
                if message == 'нравится':
                    favorites.append([event.user_id, *vk_inf.get_inf()])
                    print(favorites)
                elif message == 'стоп':
                    break
