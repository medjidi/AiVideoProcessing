# pip install opencv-python
# pip install tensorflow
# https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API#usage

import cv2 as cv
import tensorflow as tf
import asyncio
import concurrent.futures

# Флаг для остановки обработки
stop_processing = False

# Загрузка модели
with tf.io.gfile.GFile('model/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb', 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())


# получение картинки по ссылке
def load_image(image_path):
    image = cv.imread(image_path)  # сама картинка
    rows = image.shape[0]  # высота картинки
    cols = image.shape[1]  # ширина картинки
    inp = cv.resize(image, (300, 300))  # будущий батч изображения
    inp = inp[:, :, [2, 1, 0]]  # BGR2RGB
    return image, inp, rows, cols


def run_inference(sess, inp):
    out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                    sess.graph.get_tensor_by_name('detection_scores:0'),
                    sess.graph.get_tensor_by_name('detection_boxes:0'),
                    sess.graph.get_tensor_by_name('detection_classes:0')],
                   feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
    return out


def process_image(sess, image_path):
    if stop_processing:
        raise asyncio.CancelledError()

    image, inp, rows, cols = load_image(image_path)
    out = run_inference(sess, inp)  # получение готовой сессии модели со всеми детекциями
    detections = []  # массив детекций внутри этой сессии

    # путём нехитрых манипуляций извлекаем информацию из сессии и оставляем только детекции с людьми
    num_detections = int(out[0][0])
    for i in range(num_detections):
        classId = int(out[3][0][i])
        score = float(out[1][0][i])
        bbox = [float(v) for v in out[2][0][i]]
        if score > 0.3 and classId == 1:  # Класс 1 соответствует "человеку" в COCO
            x = bbox[1] * cols
            y = bbox[0] * rows
            right = bbox[3] * cols
            bottom = bbox[2] * rows

            detections.append([x, y, right, bottom])  # добавляем координаты в массив текущей сессии
            # cv.rectangle(image, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
            # cv.putText(image, 'Person', (int(x), int(y) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image_path, detections


async def main(image_paths):
    global stop_processing  # это для отслежки остановки обработки
    detections = []  # итоговый массив детекций

    with tf.compat.v1.Session() as sess:  # для каждой ассинхронной сессии...
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        with concurrent.futures.ThreadPoolExecutor() as executor:  # для каждого костыля для TensorFlow...
            loop = asyncio.get_event_loop()  # создаём петлю...
            tasks = [
                loop.run_in_executor(executor, process_image, sess, image_path)  # в которой запускаем обработки кадров...
                for image_path in image_paths  # для каждого кадра из списка по ссылкам.
            ]
            try:
                for result in await asyncio.gather(*tasks):  # запуск потоков для каждого пафа
                    detections.append(result)
            except asyncio.CancelledError:
                print("Processing was cancelled")

    print("Обнаруженные прямоугольники:", detections)

# Пример использования
image_paths = ["images/001.jpg", "images/002.jpg", "images/003.jpg", "images/004.jpg"]
asyncio.run(main(image_paths))
