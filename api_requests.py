# pip install requests

import requests


# метод на отправу post с ссылкой на видео reference_video
def post_request_send_video(reference_video):
    url = "http://127.0.0.1:8000/post-request-send-video/"  # ссылка запроса
    params = {"reference": reference_video}  # Передача ссылки на видео в параметрах запроса
    try:

        response = requests.post(url, params=params)  # Отправка данных в формате JSON
        response.raise_for_status()  # Проверка на наличие ошибок HTTP
        print("POST запрос на отправку видео успешно отправлен")

    except requests.exceptions.RequestException as e:

        print(f"Ошибка при отправке POST запроса на отправку видео: {e}")
        if response is not None:
            print(f"Статус код: {response.status_code}")
            print(f"Ответ сервера: {response.text}")


def post_request_stop():
    url = "http://127.0.0.1:8000/post-request-stop/"  # ссылка запроса
    try:

        response = requests.post(url)  # отправка запроса
        if response.status_code == 200:  # проверка успешности запроса
            print("POST запрос на остановку обработки успешно отправлен")
        else:
            print("Ошибка при отправке POST запроса на остановку обработки")

    except requests.exceptions.RequestException as e:

        print(f"Ошибка при отправке POST запроса на отправку видео: {e}")
        if response is not None:
            print(f"Статус код: {response.status_code}")
            print(f"Ответ сервера: {response.text}")


def get_request_result():
    url = "http://127.0.0.1:8000/get-request-result/"
    try:

        response = requests.get(url)  # отправка запроса
        if response.status_code == 200:  # проверка статуса запроса
            data = response.json()  # получение json из запроса
            array = data["array"]  # получение массива детекции из json'а
        else:
            print("Ошибка при отправке GET запроса на получение результата обработки")
        return array

    except requests.exceptions.RequestException as e:

        print(f"Ошибка при отправке POST запроса на отправку видео: {e}")
        if response is not None:
            print(f"Статус код: {response.status_code}")
            print(f"Ответ сервера: {response.text}")


def get_request_state():
    url = "http://127.0.0.1:8000/get-request-state/"
    try:

        response = requests.get(url)  # отправка запроса
        if response.status_code == 200:  # проверка статуса запроса
            data = response.json()  # получение json из запроса
            state = data["state"]  # получение статуса из json'а
        else:
            print("Ошибка при отправке GET запроса на получение статуса обработки")
        return state

    except requests.exceptions.RequestException as e:

        print(f"Ошибка при отправке POST запроса на отправку видео: {e}")
        if response is not None:
            print(f"Статус код: {response.status_code}")
            print(f"Ответ сервера: {response.text}")
