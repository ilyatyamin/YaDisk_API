import consts
from yadisk.yandex_disk import *

disk = YaDisk(consts.OAUTH_TOKEN)

print(disk.move_file('folder_new/folder', 'folder'))