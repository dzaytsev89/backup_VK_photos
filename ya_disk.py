import requests


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
        # pprint(response.json())
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
        # pprint(response.json())
        if response.status_code == 201:
            # print("Success - 201")
            pass
        else:
            print('Error! ', response.status_code)

    # def _get_upload_link(self, disk_file_path):
    #     upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    #     headers = self.get_headers()
    #     params = {"path": disk_file_path, "overwrite": "true"}
    #     response = requests.get(upload_url, headers=headers, params=params)
    #     # pprint(response.json())
    #     return response.json()
    #
    # def upload_file_to_disk(self, disk_file_path, filename):
    #     href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
    #     response = requests.put(href, data=open(filename, 'rb'))
    #     response.raise_for_status()
    #     if response.status_code == 201:
    #         print("Success")

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
