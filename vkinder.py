import random
import requests
import time
from Token import USER_ID, personal_token  # персональный токен

access_token = personal_token


class VKinder_get_info:

    def __init__(self, sex, age, city):
        global status_
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
            'count': 1,
            'offset': random.randrange(0, 100),
            'sort': 0,
            "fields": 'sex, city, photo_id, screen_name',
            "age_from": age - 3,
            "age_to": age + 3,
            "sex": sex_,
            "hometown": city,
            "status": 1,
            "album_id": "profile"
        }

    """Получаем информацию для запроса урла фото"""

    def get_inf(self):
        result = []
        while True:
            url_get_info = self.vk_url + "users.search?"
            req = requests.get(url_get_info, params=self.params).json()
            time.sleep(0.1)
            if req['response']['items'] is not None:
                for item in req['response']['items']:
                    time.sleep(0.1)
                    if item['is_closed'] is False:
                        result.append([item['first_name'], item['last_name'], item['id'],
                                       f"https://vk.com/{item['screen_name']}"])
                    else:
                        result.append([item['first_name'], item['last_name'], item['id'],
                                       f"https://vk.com/{item['screen_name']} - Закрытый профиль!"])
                    break
                else:
                    continue
            if len(result) != 0:
                break
        return result


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
                attachment.append(f'https://vk.com/photo{self.owner_id}_{item["id"]}')
        return attachment
