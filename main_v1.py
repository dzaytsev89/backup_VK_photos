import json
import time
import vk_class
import ya_disk

# TOKENS
vk_token = ''

def main():
    def closed_vk_id():
        status = vk_cl.users_info()
        if status['response'][0]['can_access_closed']:
            return True
        else:
            print('Профиль закрыт, невозможно скачать фото без соответствующего токена')
            return False

    def _check_dir_vk_id(path):
        vk_id_backup_folders = ya.find_folders(path)
        if vk_id not in vk_id_backup_folders:
            ya.create_dir(path + vk_id)
            return print("Папка для записи фото создана")
        else:
            return print("Папка для записи фото существует")

    def copy_vk_avatars_to_ya(path, count):
        counter = int(count)
        if len(vk_cl.largest_avatars()) < int(count):
            print(f'Нет столько фотографий в альбоме, будет скопировано {len(vk_cl.largest_avatars())} фотографий')
            counter = len(vk_cl.largest_avatars())
        _check_dir_vk_id(path)
        photo_log = dict()
        photo_log['photos'] = []
        for photo in vk_cl.largest_avatars():
            if counter == 0:
                print(f'Загружено {count} фотографий')
                print(f'Информацию о загруженных фотографиях можно посмотреть в файле loaded_photos_{vk_id}.json')
                return
            else:
                file_name = photo['likes'] + '.jpeg'
                if photo['likes'] + '.jpeg' in ya.get_files_list_name(path + vk_id):  # check_filename
                    file_name = photo['likes'] + '_' + photo['date'] + '.jpeg'
                somedict = dict()
                somedict['file_name'] = file_name
                somedict['size'] = photo['type']
                photo_log['photos'].append(somedict)
                file_path = path + vk_id + '/' + file_name
                ya.upload_file_from_url(file_url=photo['largest_url'], disk_path=file_path)
                time.sleep(1)
            counter -= 1
            with open(f"loaded_photos_{vk_id}.json", "w") as f:
                json.dump(photo_log, f)
        print(f'Информацию о загруженных фотографиях можно посмотреть в файле loaded_photos_{vk_id}.json')

    def copy_vk_foto_to_ya(path, count):
        counter = int(count)
        if len(vk_cl.largest_foto(album_type=album_type)) < int(count):
            print(f'Нет столько фотографий в альбоме, будет скопировано {len(vk_cl.largest_foto(album_type))} фотографий')
            counter = len(vk_cl.largest_foto(album_type))
        _check_dir_vk_id(path)
        photo_log = dict()
        photo_log['photos'] = []
        for photo in vk_cl.largest_foto(album_type):
            if counter == 0:
                print(f'Загружено {count} фотографий')
                print(f'Информацию о загруженных фотографиях можно посмотреть в файле loaded_photos_{vk_id}.json')
                return
            else:
                file_name = photo['likes'] + '.jpeg'
                if photo['likes'] + '.jpeg' in ya.get_files_list_name(path + vk_id):  # check_filename
                    file_name = photo['likes'] + '_' + photo['date'] + '.jpeg'
                somedict = dict()
                somedict['file_name'] = file_name
                somedict['size'] = photo['type']
                photo_log['photos'].append(somedict)
                file_path = path + vk_id + '/' + file_name
                ya.upload_file_from_url(file_url=photo['largest_url'], disk_path=file_path)
                time.sleep(1)
            counter -= 1
            with open(f"loaded_photos_{vk_id}.json", "w") as f:
                json.dump(photo_log, f)
        print(f'Информацию о загруженных фотографиях можно посмотреть в файле loaded_photos_{vk_id}.json')

    while True:
        # INPUT DATA
        vk_id = input('Введите vk_id: ')
        vk_cl = vk_class.VK(vk_token, vk_id)
        if closed_vk_id():
            pass
        else:
            continue
        print('''Введите альбом из которого хотите скачать фото (по умолчанию - аватарки)
        доступно для выбора:
        profile - аватарки
        wall - фотографии со страницы
        saved - сохранённые фото''')
        album_type = input()
        if album_type == '': album_type = 'profile'
        ya_token = input('Введите yandex_token: ')
        ya = ya_disk.YandexDisk(token=ya_token)
        dest_path = input('Введите путь к папке, куда необходимо сохранить фотографии (По умолчанию в :/) :')
        photo_count = input('Введите количество фотографий которые необходимо скопировать(по умолчанию 5) : ')
        if dest_path == '': dest_path = '/'
        if photo_count == '': photo_count = 5

        if __name__ == '__main__':
            # copy_vk_avatars_to_ya(path=dest_path, count=photo_count)
            copy_vk_foto_to_ya(path=dest_path, count=photo_count)
    # print('check_photo_log')
    # with open(f"loaded_photos_{vk_id}.json") as f:
    #     json_data = json.load(f)
    #     print(pd.DataFrame(json_data))


if __name__ == '__main__':
    main()
