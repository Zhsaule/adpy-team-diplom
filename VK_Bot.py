import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from auth_data import GROUP_TOKEN
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
longpool = VkLongPoll(vk_session)


def to_listen(message):
    for item in longpool.listen():
        if item.type == VkEventType.MESSAGE_NEW:
            if item.to_me:
                message = item.text.lower()
                return message

def write_msg(user_id, message, keyboard=None):
    post = {'user_id': user_id, 'message': message, 'random_id': 0}

    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()

    vk_session.method('messages.send', post)


# favorites = []
user_info = []


def bot():
    # global vk_inf, message, info
    key_word = ['старт', 'далее', '❤', '❤❤❤', 'стоп', 'авто', 'запрос', 'стоп']
    longpool = VkLongPoll(vk_session)
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                find_keyboard = VkKeyboard(inline=True)
                find_keyboard.add_button("❤", VkKeyboardColor.PRIMARY)
                find_keyboard.add_button("Далее", VkKeyboardColor.PRIMARY)
                find_keyboard.add_button("Стоп", VkKeyboardColor.PRIMARY)
                message = event.text.lower()
                print(f'main {message}')

                if str(message) == 'запрос':
                    write_msg(event.user_id, f'Введите город, возраст,\n'
                                             f'пол(м/ж) через запятую или пробел:')
                    # print(f'if1 запрос  {message}')

                if str(message) == 'авто':
                    print(f'if2 авто  {message}')
                    try:
                        auto_string = get_user_param(event.user_id)
                        auto_keyboard = VkKeyboard(inline=True)
                        auto_keyboard.add_button(auto_string, VkKeyboardColor.PRIMARY)
                        write_msg(event.user_id, f'Подбор для вас\n'
                                                 f'по вашим данным:', auto_keyboard)
                    except:
                        KeyError("Заполните в профиле ваши данные: пол, дату и год рождения!")
                        write_msg(event.user_id, 'Проверьте правильность набора. Введите: город, возраст, пол(м/ж).',
                                  main_keyboard)

                if len(message.split(',')) == 1 and message not in key_word:
                    message = ",".join(message.split(" "))
                    print(f'if3 ,-пробел  {message}')
                if len(message.split(',')) == 3 and message not in key_word:
                    # ('старт', 'далее', '❤', '❤❤❤', 'стоп', 'авто', 'запрос'):
                    response = message.split(",")
                    response = [i.strip().title() for i in response]
                    city, age, sex = response
                    print(f'if4 response: {response} message:{message}')

                if len(message.split(',')) != 3 and message not in key_word:
                    # ('старт', 'далее', '❤', '❤❤❤', 'стоп', 'авто', 'запрос'):
                    write_msg(event.user_id, 'Проверьте правильность набора1. Введите: город, возраст, пол(м/ж).',
                              main_keyboard)
                    print(f'if5 !=3  {message}')
                elif len(message.split(',')) == 3 or message == 'далее':
                    print(f'elif5 ==3 and далее {response} message {message}')

                    if age.isdigit() is True:
                        if int(age) < 16:
                            write_msg(event.user_id, "Возрастное ограничение 16+")
                        else:
                            print(f'sex {sex} age {age} city {str(city.title())} user id {event.user_id}')
                            info = VKinder_get_info(str(sex).lower(), int(age), str(city.title())).get_inf(
                                event.user_id)
                            # сохраняем пользовательские данные в таб. Users
                            ins_data(event.user_id, int(age), str(sex).lower(), str(city.title()))
                            if info is None:
                                write_msg(event.user_id,
                                          'Проверьте правильность набора2. Введите: город, возраст, пол(м/ж)')
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
                                    write_msg(event.user_id, f'Нажмите копку " ❤ ", если нравится;\n'
                                                             f'"Далее" для продолжения поиска;\n'
                                                             f'"Стоп" выход.', find_keyboard)

                                else:
                                    write_msg(event.user_id, "Не найдено совпадений. Попробуйте еще раз!",
                                              main_keyboard)
                    else:
                        write_msg(event.user_id,
                                  'Проверьте правильность набора3. Введите: город, возраст, ваш пол(м/ж)')

                print(f'end user_info {user_info}')
                if message == '❤':
                    favor_keyboard = VkKeyboard(inline=True)
                    favor_keyboard.add_button("Далее", VkKeyboardColor.PRIMARY)
                    favor_keyboard.add_button("Стоп", VkKeyboardColor.PRIMARY)
                    photos = VKinder_get_photo(info[2]).get_photo_url()
                    # добавдяем данные понравившегося человека в "Избранное"
                    ins_fav_data(event.user_id, info[2], info[0], info[1], info[3], photos)
                    # favorites.append([event.user_id, info])
                    write_msg(event.user_id, f'❤ сохранили в Избранное ;\n', favor_keyboard)

                elif str(message) == '❤❤❤':
                    write_msg(event.user_id, f'❤ Ваш список избранных ❤')
                    favor_lst_keyboard = VkKeyboard(inline=True)
                    favor_lst_keyboard.add_button("Далее", VkKeyboardColor.PRIMARY)
                    favor_lst_keyboard.add_button("Стоп", VkKeyboardColor.PRIMARY)
                    write_msg(event.user_id, f'Нажмите "Далее" для продолжения', favor_lst_keyboard)
                    favorites = select_fav_client(event.user_id)
                    cnt_fav = len(favorites)
                    print(cnt_fav)
                    j = 0
                    for event in longpool.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            message = event.text.lower()
                            if message == 'далее':
                                write_msg(event.user_id, f'{favorites[j][2]} {favorites[j][1]} - {favorites[j][3]}')
                                for i in favorites[j][4].split(","):
                                    i = i.replace('{', '').replace('}', '')
                                    print(f'fav - {i}')
                                    MessagesSend(event.user_id, i).send_photo()
                                j += 1
                                write_msg(event.user_id, f'"Далее" для продолжения, или "Стоп" для выхода'
                                          , favor_lst_keyboard)
                            elif message == 'стоп':
                                write_msg(event.user_id, f'введите Авто для автоподбора,\n'
                                                         f'Запрос для выбора по запросу,\n'
                                                         f'❤❤❤ для просмотра своего списка Избранных.', main_keyboard)
                                bot()

                elif message == 'стоп':
                    write_msg(event.user_id, f'Поиск окончен 👋\n'
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
                        write_msg(event.user_id, f'введите Авто для автоподбора,\n'
                                                 f'Запрос для выбора по запросу,\n'
                                                 f'❤❤❤ для просмотра своего списка Избранных.', main_keyboard)

                        return bot()

                    else:
                        write_msg(event.user_id, f'Привет 🤗\n'
                                                 f'Vkinder6 приветствует Вас!\n'
                                                 f'Хотите с кем нибудь пообщаться?\n'
                                                 f'Введите "Старт"', start_keyboard)

                        continue
