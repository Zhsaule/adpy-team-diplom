import random
import requests
from Token import GROUP_TOKEN, personal_token  # персональный токен

access_token = personal_token


class VKinder_get_info:

    def __init__(self, sex, age, city):
        self.sex = sex
        self.age = age
        self.city = city.title()
        if sex == 'ж':
            sex_ = 2
        elif sex == 'м':
            sex_ = 1
        else:
            sex_ = 0
        self.vk_url = 'https://api.vk.com/method/'
        self.params = {
            "access_token": access_token,
            "v": 5.131,
            'oauth': 1,
            'count': 100,
            'offset': random.randrange(0, 100),
            'sort': 0,
            "fields": 'sex, city, photo_id, screen_name, can_write_private_message',
            "age_from": age - 3,
            "age_to": age + 3,
            "sex": sex_,
            "hometown": city,
            "status": 1,
            "album_id": "profile"
        }

    """Получаем информацию для запроса урла фото"""

    def _get_all_result(self):
        url_get_info = self.vk_url + "users.search?"
        req = requests.get(url_get_info, params=self.params).json()
        all_result_list = [req['response']['items']]
        return all_result_list

    def get_inf(self):
        try:
            all_result_list = self._get_all_result()
            for items in all_result_list:
                for i in range(len(items)):
                    item = items[i]
                    if item['is_closed'] is False and item['can_write_private_message'] == 1:
                        print(item)
                        result = item['first_name'], item['last_name'], item[
                            'id'], f"https://vk.com/{item['screen_name']}"
                        return result
                    else:
                        continue
        except:
            KeyError("Проверьте правильность набора!")
        return None


class VKinder_get_photo:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.vk_url = 'https://api.vk.com/method/'
        self.params = {
            "access_token": access_token,
            "v": 5.131,
            'oauth': 1,
            "owner_id": owner_id,
            "album_id": "profile",
            "photo_sizes": 1,
            "extended": 1
        }

    def get_photo_url(self):
        url_photos_get = self.vk_url + "photos.get?"
        req = requests.get(url_photos_get, params=self.params).json()
        attachment = []
        if 'response' in req.keys() and len(req['response']['items']) != 0:
            photos = sorted(req['response']['items'], key=lambda k: k['likes']['count'], reverse=True)
            if len(photos) > 3:
                photos = photos[:3]
            for item in photos:
                attachment.append(f'photo{self.owner_id}_{item["id"]}')
        return attachment


class MessagesSend:

    def __init__(self, user_id, item):
        self.vk_url = 'https://api.vk.com/method/'
        self.user_id = user_id
        self.params = {
            "access_token": GROUP_TOKEN,
            "user_id": self.user_id,
            "peer_id": self.user_id,
            "attachment": item,
            "v": 5.131,
            "random_id": 0
        }

    def send_photo(self):
        url_send_message = self.vk_url + "messages.send?"
        req = requests.post(url_send_message, params=self.params).json()
        return req




