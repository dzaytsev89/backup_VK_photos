import requests
import vk_class
import time


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self, path):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.get(files_url, headers=headers, params=params)
        return response.json()

    def get_files_list_name(self, path):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.get(files_url, headers=headers, params=params)
        items = response.json()['_embedded']['items']
        names = []
        for i in items:
            names.append(i['name'])
        return names

    def find_folders(self, path):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.get(files_url, headers=headers, params=params)
        folders = response.json()['_embedded']['items']
        ids_folders = []
        for folder in folders:
            if folder['type'] == 'dir':
                ids_folders.append(folder['name'])
        return ids_folders

    def create_dir(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.put(headers=headers, url=url, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            pass
        else:
            print('Error! ', response.status_code)

    def upload_file_from_url(self, file_url, disk_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {"path": disk_path, "url": file_url}   # url - from which url, path - to which path on disk
        headers = self.get_headers()
        response = requests.post(url=url, headers=headers, params=params)
        response.raise_for_status()
        # pprint(response.json())
        if response.status_code == 202:
            print(f"File {disk_path.split('/')[-1]} uploaded!")
        else:
            print('Error!', response.status_code)

    def check_dir_vk_id(self, vk_id, path):
        vk_id_backup_folders = self.find_folders(path)
        if vk_id not in vk_id_backup_folders:
            self.create_dir(path + vk_id)
            return print("Папка для записи фото создана")
        else:
            return print("Папка для записи фото существует")

    def copy_vk_photo_to_ya(self, path, count, album_type, vk_client, photo_log):
        counter = int(count)
        photo_bank = vk_class.VK.largest_photo(vk_client, album_type=album_type)
        print(photo_bank)
        if len(photo_bank) < int(count):
            print(f'Нет столько фотографий в альбоме, будет скопировано'
                  f' {len(photo_bank)} фотографий')
            counter = len(photo_bank)
        self.check_dir_vk_id(vk_id=vk_client.vk_id, path=path)
        # photo_log = dict()
        # photo_log['photos'] = []
        # pprint(sorted(photo_bank, key=lambda like: int(photo_bank['likes']))[::-1])
        for photo in photo_bank:
            if counter != 0:
                file_name = photo['likes'] + '.jpeg'
                if photo['likes'] + '.jpeg' in self.get_files_list_name(path + vk_client.vk_id):  # check_filename
                    file_name = photo['likes'] + '_' + photo['date'] + '.jpeg'
                some_dict = dict()
                some_dict['file_name'] = file_name
                some_dict['size'] = photo['type']
                photo_log.append(some_dict)
                file_path = path + vk_client.vk_id + '/' + file_name
                self.upload_file_from_url(file_url=photo['largest_url'], disk_path=file_path)
                time.sleep(2)
            else:
                print(f'Загружено {count} фотографий')
                print(f'Информацию о загруженных фотографиях можно посмотреть'
                      f' в файле loaded_photos_{vk_client.vk_id}.json')
                return photo_log
            counter -= 1
