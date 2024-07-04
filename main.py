import consts
from yadisk.yandex_disk import *

disk = YaDisk(consts.OAUTH_TOKEN)

print(disk.create_directory('empty_folder/'))