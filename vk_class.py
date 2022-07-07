import requests
import datetime


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, user_id, version='5.131'):
        self.token = vk_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        params = {'user_ids': self.id}
        response = requests.get(self.url + 'users.get', params={**self.params, **params})
        return response.json()

    def photos_get_profile(self):
        params = {'album_id': 'profile', 'extended': '1', 'owner_id': self.id}
        req = requests.get(self.url + 'photos.get', params={**self.params, **params}).json()
        # print(req['response'])
        avatar_albums = req['response']['items']
        return avatar_albums

    def photos_get(self, album_id):
        params = {'album_id': album_id, 'extended': '1', 'owner_id': self.id}
        req = requests.get(self.url + 'photos.get', params={**self.params, **params}).json()
        # print(req['response'])
        avatar_albums = req['response']['items']
        return avatar_albums

    def largest_avatars(self):
        avatars = self.photos_get_profile()
        id_photos = []
        for album in avatars:
            photo_cache = dict()
            photo_cache['id'] = str(album['id'])
            photo_cache['likes'] = str(album['likes']['count'])
            photo_cache['date'] = datetime.datetime.fromtimestamp(album['date']).strftime('%Y-%m-%d_%H-%M-%S')
            # print(sorted(album['sizes'], key=lambda type: type['type']))
            for size in album['sizes']:
                if size['type'] == 'w':
                    photo_cache['largest_url'] = size['url']
                    photo_cache['type'] = size['type']
                else:
                    photo_cache['largest_url'] = sorted(album['sizes'], key=lambda type: type['type'])[-1]['url']
                    photo_cache['type'] = size['type']
            id_photos.append(photo_cache)
        return id_photos

    def largest_foto(self, album_type):
        avatars = self.photos_get(album_id=album_type)
        id_photos = []
        for album in avatars:
            photo_cache = dict()
            photo_cache['id'] = str(album['id'])
            photo_cache['likes'] = str(album['likes']['count'])
            photo_cache['date'] = datetime.datetime.fromtimestamp(album['date']).strftime('%Y-%m-%d_%H-%M-%S')
            # print(sorted(album['sizes'], key=lambda type: type['type']))
            for size in album['sizes']:
                if size['type'] == 'w':
                    photo_cache['largest_url'] = size['url']
                    photo_cache['type'] = size['type']
                else:
                    photo_cache['largest_url'] = sorted(album['sizes'], key=lambda type: type['type'])[-1]['url']
                    photo_cache['type'] = size['type']
            id_photos.append(photo_cache)
        return id_photos
