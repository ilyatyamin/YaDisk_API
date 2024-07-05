import json

import consts
from yadisk.yandex_disk import *

disk = YaDisk(consts.OAUTH_TOKEN)

disk.download_file('Хлебные крошки.mp4', '/Users/mrshrimp.it/Desktop')