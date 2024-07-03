from typing import Dict, Optional

import requests
import json
from flask import Flask
from yadisk.__constants import *
from yadisk.__interface import *
from yadisk.exceptions.IncorrectDataError import IncorrectDataError
from yadisk.exceptions.InvalidTokenError import InvalidTokenError
from yadisk.exceptions.ServerError import ServerError


class YaDisk(FileExplorerInterface):
    def __init__(self, oauth_token: str):
        super().__init__()
        app = Flask(__name__)

        @app.route("/", methods=["GET"])
        def main():
            return AUTH_PAGE

        @app.route("/callback", methods=["POST"])
        def callback():
            pass

        # app.run("127.0.0.1", 8298, threaded=False)
        self._auth(oauth_token)

    def upload_file(self, loc_path, dist_path):
        pass

    def download_file(self, dist_path, loc_path):
        pass

    def make_folder(self, dist_path):
        pass

    def delete_file(self, dist_path):
        pass

    def delete_directory(self, dist_path):
        pass

    def file_exists(self, dist_path: str) -> bool:
        """
        :param dist_path: path to the file on Yandex disk
        :return: True if directory with path dist_path exists, else returns False

        Throws:
        - **InvalidTokenError**, if your token is not valid
        """
        response = requests.request(method='GET',
                                    url=f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:/{dist_path}',
                                    headers=self._get_headers())
        info = self._process_str_to_dict(response.text)

        if response.status_code == 200:
            return info.get('type') == 'file'
        elif response.status_code == 401:
            raise InvalidTokenError(additional_info=info['message'])
        else:
            return False

    def dir_exists(self, dist_path: str) -> bool:
        """
        :param dist_path: path to the dir on Yandex disk
        :return: True if directory with path dist_path exists, else returns False

        Throws:

        - **InvalidTokenError**, if your token is not valid
        """
        response = requests.request(method='GET',
                                    url=f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:/{dist_path}',
                                    headers=self._get_headers())
        info = self._process_str_to_dict(response.text)

        if response.status_code == 200:
            return info.get('type') == 'dir'
        elif response.status_code == 401:
            raise InvalidTokenError(additional_info=info['message'])
        else:
            return False

    def move_file(self, src_path: str, dst_path: str,
                  overwrite_allowed: bool = True) -> str:
        """
        Moves a file from one location to another.
        :param src_path: path where the folder or file is currently located
        :param dst_path: path where you want to move the folder or file
        :param overwrite_allowed: True if overwriting is allowed else False
        :return: new link to an object on Yandex Disk

        Throws:

        - **InvalidTokenError**, if your token is not valid
        - **IncorrectDataError**, if your data is incorrect (path is incorrect, the size of file / dir if too high, etc.)
        - **ServerError** in other cases
        """
        response = requests.request(method='POST',
                                    url=f'https://cloud-api.yandex.net/v1/disk/resources/move?from={src_path}&path={dst_path}&overwrite={self._bool_to_str(overwrite_allowed)}',
                                    headers=self._get_headers())
        info = self._process_str_to_dict(response.text)

        if str(response.status_code)[0] == '2':  # 200, 201, 202, ...
            return info.get('href', None)
        elif str(response.status_code)[0] == '4' and response.status_code != 401:  # 400, 403, 406...
            raise IncorrectDataError(error_name=info.get('error', None),
                                     additional_info=info.get('message', None))
        elif response.status_code == 401:
            raise InvalidTokenError(additional_info=info['message'])
        else:
            raise ServerError(info['message'])

    def get_link(self, dist_path):
        """
        :param dist_path: path to the object on Yandex disk
        :return: link to an object on Yandex Disk
        Using the local path of the file on Yandex Disk, it receives its link on the network.

        Throws

        - **IncorrectDataError**, if you send incorrect data
        - **InvalidTokenError**, if your token is not valid
        - **FileNotFoundError**, if your file is not exists
        - **ServerError**, in other cases
        """
        response = requests.request(method='GET',
                                    url=f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:/{dist_path}',
                                    headers=self._get_headers())
        info = self._process_str_to_dict(response.text)
        if response.status_code == 200:
            if 'public_url' in info:
                return info['public_url']
            else:
                raise ServerError("This file doesn't have public link.")
        elif response.status_code == 400:
            raise IncorrectDataError(error_name=info['error'],
                                     additional_info=info['message'])
        elif response.status_code == 401:
            raise InvalidTokenError(additional_info=info['message'])
        elif response.status_code == 404:
            raise FileNotFoundError(info['message'])
        else:
            raise ServerError(info['message'])

    def _auth(self, token):
        self.__oauth_token__ = token
        if not isinstance(token, str):
            raise InvalidTokenError()

    def _get_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.__oauth_token__}'
        }

    @staticmethod
    def _process_str_to_dict(raw_data: str) -> Dict[str, str]:
        return json.loads(raw_data)

    @staticmethod
    def _bool_to_str(value: bool) -> str:
        if value:
            return "true"
        else:
            return "false"
