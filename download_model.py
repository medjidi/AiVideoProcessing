import urllib.request
import tarfile

# URL для загрузки модели
model_url = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"

# Путь для сохранения архива модели
save_path = "C:/Users/65696/PycharmProjects/Python6sem/ssd_mobilenet_v2_coco.tar.gz"

# Скачивание архива модели
urllib.request.urlretrieve(model_url, save_path)

# Распаковка архива модели
with tarfile.open(save_path, 'r:gz') as tar:
    tar.extractall("path_to_save_directory")
