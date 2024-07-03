from flask import Flask
from yadisk.__constants import *
from yadisk.__interface import *
from yadisk.exceptions.InvalidTokenException import InvalidTokenException


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

        app.run("127.0.0.1", 8298)
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

    def file_exists(self, dist_path):
        pass

    def dir_exists(self, dist_path):
        pass

    def move_file(self, src_path, dst_path):
        pass

    def get_link(self, dist_path):
        pass

    def _auth(self, token):
        self.__oauth_token__ = token
        if not isinstance(token, str):
            raise InvalidTokenException()