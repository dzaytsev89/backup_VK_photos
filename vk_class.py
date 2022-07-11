import requests
import datetime


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, user_id, version='5.131'):
        self.token = vk_token
        self.vk_id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        params = {'user_ids': self.vk_id}
        response = requests.get(self.url + 'users.get', params={**self.params, **params})
        return response.json()

    def photos_get(self, album_id):
        params = {'album_id': album_id, 'extended': '1', 'owner_id': self.vk_id}
        req = requests.get(self.url + 'photos.get', params={**self.params, **params}).json()
        photo_albums = req['response']['items']
        return photo_albums

    def largest_photo(self, album_type):
        photos = self.photos_get(album_type)
        id_photos = []
        for album in photos:
            photo_cache = dict()
            photo_cache['id'] = str(album['id'])
            photo_cache['likes'] = str(album['likes']['count'])
            photo_cache['date'] = datetime.datetime.fromtimestamp(album['date']).strftime('%Y-%m-%d_%H-%M-%S')
            for size in album['sizes']:
                if size['type'] == 'w':
                    photo_cache['largest_url'] = size['url']
                    photo_cache['type'] = size['type']
                else:
                    photo_cache['largest_url'] = sorted(album['sizes'], key=lambda type_: type_['type'])[-1]['url']
                    photo_cache['type'] = size['type']
            id_photos.append(photo_cache)
        return id_photos

    def closed_vk_id(self):
        status = self.users_info()
        if status['response'][0]['can_access_closed']:
            return True
        else:
            print('Профиль закрыт, невозможно скачать фото без соответствующего токена')
            return False

    def find_vk_id(self):
        info = self.users_info()
        return str(info['response'][0]['id'])
