import vk_class
import ya_disk
import configparser
import json


# TOKENS
tokens = configparser.ConfigParser()
tokens.read("tokens.ini")
token = tokens['tokens']
ya_token = ya_disk.YandexDisk(token['ya_token'])
vk_token = token['vk_token']


def json_logger(photo_log, vk_id):
    with open(f"loaded_photos_{vk_id}.json", "w") as f:
        json.dump(photo_log, f)


def main():

    while True:
        photo_log = list()
        # INPUT DATA
        vk_screen_name = input('Введите vk_id или vk_screen_name: ')
        vk_cl = vk_class.VK(vk_token=vk_token, user_id=vk_screen_name)
        vk_cl.vk_id = vk_class.VK.find_vk_id(vk_cl)
        if not vk_class.VK.closed_vk_id(vk_cl):
            continue
        else:
            pass
        print('''Введите альбом из которого хотите скачать фото (по умолчанию - аватарки)
        доступно для выбора:
        profile - аватарки
        wall - фотографии со страницы
        saved - сохранённые фото''')
        album_type = input()
        if album_type == '':
            album_type = 'profile'
        dest_path = input('Введите путь к папке, куда необходимо сохранить фотографии (По умолчанию в :/) :')
        photo_count = input('Введите количество фотографий которые необходимо скопировать(по умолчанию 5) : ')
        if dest_path == '':
            dest_path = '/'
        if photo_count == '':
            photo_count = 5
        ya_disk.YandexDisk.copy_vk_photo_to_ya(ya_token, path=dest_path, vk_client=vk_cl,
                                               count=photo_count, album_type=album_type, photo_log=photo_log)
        json_logger(photo_log=photo_log, vk_id=vk_cl.vk_id)

        # pprint(photo_log)
    # with open(f"loaded_photos_{vk_id}.json") as f:
    #     json_data = json.load(f)
    #     print(pd.DataFrame(json_data))


if __name__ == '__main__':
    main()
