import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from team.token import GROUP_TOKEN
from vkinder import VKinder_get_info, VKinder_get_photo, get_user_param
from vkinder import MessagesSend
from Data.ins_data import ins_data, ins_fav_data, ins_propose_data, select_fav_client

vk_session = vk_api.VkApi(token=GROUP_TOKEN)
start_keyboard = VkKeyboard(inline=True)
start_keyboard.add_button("Старт", VkKeyboardColor.PRIMARY)
main_keyboard = VkKeyboard(inline=True)
main_keyboard.add_button("Авто", VkKeyboardColor.PRIMARY)
main_keyboard.add_button("Запрос", VkKeyboardColor.PRIMARY)
main_keyboard.add_button("❤❤❤", VkKeyboardColor.PRIMARY)
find_keyboard = VkKeyboard(inline=True)
find_keyboard.add_button("❤", VkKeyboardColor.PRIMARY)
find_keyboard.add_button("Далее", VkKeyboardColor.PRIMARY)
find_keyboard.add_button("Стоп", VkKeyboardColor.PRIMARY)
next_keyboard = VkKeyboard(inline=True)
next_keyboard.add_button("Далее", VkKeyboardColor.PRIMARY)
next_keyboard.add_button("Стоп", VkKeyboardColor.PRIMARY)


def write_msg(user_id, message, keyboard=None):
    post = {'user_id': user_id, 'message': message, 'random_id': 0}

    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()

    vk_session.method('messages.send', post)


# favorites = []
user_info = []


def bot():
    key_word = ['старт', '❤', '❤❤❤', 'стоп', 'авто', 'запрос']
    req_err = False
    longpool = VkLongPoll(vk_session)
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                print(f'main {message}')

                if str(message) == 'запрос':
                    print('if Запрос')
                    write_msg(event.user_id, f'Введите город, возраст,\n'
                                             f'пол(м/ж) через запятую или пробел:')

                if str(message) == 'авто':
                    print('if Авто')
                    try:
                        auto_string = get_user_param(event.user_id)
                        auto_keyboard = VkKeyboard(inline=True)
                        auto_keyboard.add_button(auto_string, VkKeyboardColor.PRIMARY)
                        write_msg(event.user_id, f'Подбор по вашим данным:', auto_keyboard)
                    except KeyError:
                        KeyError("Заполните в профиле ваши данные: пол, дату и год рождения!")
                        write_msg(event.user_id, 'Проверьте свой профиль в ВК. Заполните: город, возраст, пол(м/ж).',
                                  main_keyboard)

                if message not in key_word and message != 'далее':
                    print('if not in')
                    try:
                        req_err = False
                        message = ",".join(message.split(" ")) if len(message.split(',')) == 1 else message
                        print(message)
                        print(f' split {len(message.split(","))} kkk {message}')
                        response = message.split(",")
                        response = [i.strip().title() for i in response]
                        city, age, sex = response
                        print(f' 1')

                        if sex.lower() not in ('м', 'ж'):
                            write_msg(event.user_id, 'Проверьте пол (м или ж).')
                            print(f' sex _{sex}_ {message}')
                            req_err = True
                        print(f' 1')

                        if age.isdigit() is not True:
                            write_msg(event.user_id, 'Проверьте возраст (целое число).')
                            req_err = True

                        print(f' 1')
                        if int(age) < 16:
                            write_msg(event.user_id, 'Возрастные ограничения 16.')
                            req_err = True

                        print(f' 1')
                        if len(message.split(',')) != 3:
                            print(f' split {len(message.split(","))} kkk {message}')
                            write_msg(event.user_id,
                                      'Проверьте правильность набора. Введите: город, возраст, пол(м/ж).')
                    except KeyError:
                        KeyError("Ошибка проверки введенного запроса пользователя!")
                        write_msg(event.user_id, 'Проверьте запрос1: Город, возраст, пол(м/ж).')
                        req_err = True

                if req_err is False and message not in key_word:
                    print('if req err')
                    print(f'sex {sex} age {age} city {str(city.title())} user id {event.user_id}')
                    info = VKinder_get_info(str(sex).lower(), int(age), str(city.title())).get_inf(
                        event.user_id)
                    # сохраняем пользовательские данные в таб. Users
                    ins_data(event.user_id, int(age), str(sex).lower(), str(city.title()))
                    if info is None:
                        write_msg(event.user_id, 'Не найдено совпадений. Попробуйте еще раз!', main_keyboard)
                        print(f'info None!!!!')
                    else:
                        if len(info) != 0:
                            write_msg(event.user_id, f'{info[0]} {info[1]} - {info[3]}')
                            print(info)
                            # добавляем полученные данные в таб. Propose
                            ins_propose_data(event.user_id, info[2])
                            if [f"{event.user_id}, {sex}, {age}, {city}"] not in user_info:
                                user_info.append([f"{event.user_id}, {sex}, {age}, {city}"])
                                photos = VKinder_get_photo(info[2]).get_photo_url()
                                if photos is not None:
                                    for i in photos:
                                        print(photos)
                                        MessagesSend(event.user_id, i).send_photo()
                                write_msg(event.user_id, f'Нажмите кнопку ❤, если нравится;\n'
                                                         f'"Далее" для продолжения поиска;\n'
                                                         f'"Стоп" выход.', find_keyboard)
                            else:
                                write_msg(event.user_id, "Не найдено совпадений. Попробуйте еще раз!",
                                          next_keyboard)

                if message == '❤':
                    photos = VKinder_get_photo(info[2]).get_photo_url()
                    # добавдяем данные понравившегося человека в "Избранное"
                    ins_fav_data(event.user_id, info[2], info[0], info[1], info[3], photos)
                    # favorites.append([event.user_id, info])
                    write_msg(event.user_id, f'❤ сохранили в Избранное ;\n', next_keyboard)

                elif str(message) == '❤❤❤':
                    write_msg(event.user_id, f'❤ Ваш список избранных ❤')
                    favorites = select_fav_client(event.user_id)
                    for item in favorites:
                        write_msg(event.user_id, f'{item[2]} {item[1]} - {item[3]}')
                        for i in item[4].split(","):
                            i = i.replace('{', '').replace('}', '')
                            print(f'fav - {i}')
                            MessagesSend(event.user_id, i).send_photo()
                        if str(message) == 'стоп':
                            break

                    write_msg(event.user_id, f'❤❤❤end❤❤❤', main_keyboard)

                elif message == 'стоп':
                    write_msg(event.user_id, f'Вы в основном меню 👋\n'
                                             f'❤❤❤ для просмотра своего списка Избранных\n'
                                             f'или повторите поиск', main_keyboard)


def run_bot():
    while True:
        longpool = VkLongPoll(vk_session)
        for event in longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    message = event.text.lower()

                    if str(message) == 'старт':
                        write_msg(event.user_id, f'Введите Авто для автоподбора,\n'
                                                 f'Запрос для выбора по запросу,\n'
                                                 f'❤❤❤ для просмотра своего списка Избранных.', main_keyboard)

                        return bot()

                    else:
                        write_msg(event.user_id, f'Привет 🤗\n'
                                                 f'Vkinder6 приветствует Вас!\n'
                                                 f'Хотите с кем нибудь познакомиться?\n'
                                                 f'Нажмите "Старт"!!!', start_keyboard)
