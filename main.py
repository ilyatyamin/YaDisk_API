import json

import consts
from yadisk.yandex_disk import *

disk = YaDisk(consts.OAUTH_TOKEN)

disk.upload_file('/Users/mrshrimp.it/Desktop/InternTaskE', '/')
disk.upload_file('/Users/mrshrimp.it/Desktop/files 2', '/InternTaskE/')