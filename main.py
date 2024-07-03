import consts
from yadisk.yandex_disk import *

disk = YaDisk(consts.OAUTH_TOKEN)

print(disk.file_exists("Горы.jpg"))
print(disk.file_exists("another_file.jpg"))