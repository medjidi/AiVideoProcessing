from api_requests import post_request_send_video, post_request_stop, get_request_result, get_request_state

reference_video = "didn't found yet"  # здесь будет ссылка на видео

if __name__ == "__main__":
    post_request_send_video(reference_video)
    post_request_stop()
    detections = get_request_result()
    print(detections)
    state = get_request_state()
    print(state)
