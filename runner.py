# pip install fastapi uvicorn
# cd C:\Users\65696\PycharmProjects\Python6sem
# uvicorn runner:app --reload

from fastapi import FastAPI, Query, HTTPException
import cv2

app = FastAPI()

detections = [[0, [1, 2, 3, 2]], [1, [4, 5, 6, 5]]]  # здесь будут полученные из inference детекции в виде массива
reference_video = ""  # сюда сохранится полученная по api ссылка на видео
correct_state = "nothing to do"  # здесь дубут сохраняться полученный из kafka последний статус обработки


# реализация метода получения ссыки на видео из post
@app.post("/post-request-send-video/")
async def get_reference(reference: str = Query(...)):
    global reference_video
    reference_video = reference  # извлечение ссылки на видео
    return {"message": f"reference: {reference_video}\ngot successfully."}


# реализация метода получения сигнала на остановку обработки из post
@app.post("/post-request-stop/")
async def stop_detecting():

    # здесь будет код на обработку сигнала из post об остановке обработки

    return {"message": "reference got successfully."}


# реализация метода отправки массива с детекцией ответом на get запрос
@app.get("/get-request-result/")
async def get_result():
    return {"array": detections}


# реализация метода отправки текущего статуса ответом на get запрос
@app.get("/get-request-state/")
async def get_result():
    global correct_state

    # здесь будет код получения текущего статуса обработки

    return {"state": correct_state}


# Пример URL потока с сайта Insecam
video_url = "http://96.91.239.26:1024/mjpg/video.mjpg"

# Создаем объект VideoCapture с URL
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
else:
    while True:
        ret, frame = cap.read()  # получаем кадр
        if not ret:  # проверка на то, что кард получен, т.е. не был последний
            break

        # Обработка кадра (например, отображение)
        cv2.imshow('Frame', frame)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
