from detection.detectron2_detection import Detectron2Detection 
from utils.camera_gstreamer_module import CameraGStreamerPipeline
import cv2
import time
import requests
import logging
import os

def send_telegram_notification(bot_token, chat_id, message, image_path=None):
    """
    Sends a notification to a Telegram chat with an optional image.
    """
    try:
        api_url_message=f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(api_url_message, json=payload, timeout=30)
        response.raise_for_status()
        
        if image_path:
            api_url_photo = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            with open(image_path, "rb") as photo_file:
                files = {"photo": photo_file}
                data = {"chat_id": chat_id}
                response = requests.post(api_url_photo, data=data, files=files, timeout=30)
                response.raise_for_status()
        logging.info("Notification sent succesfully")

    except requests.exceptions.RequestException as e:
        logging.error(f"Filed to send Telegram notification: {e}")

def notify_on_detection(image_path):
    """
    Callback function triggered on detection.
    """
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    message = "⚠️ Fault detected during 3D printing! ⚠️"
    CHAT_IDS = [
        1969139002,     
        1430460059,     
        52338470,
        1430460059,
    ]

    for chat_id in CHAT_IDS:
        send_telegram_notification(bot_token, chat_id, message, image_path)

def main():
    weights_file = "../data/models/model_final.pth"
    detections_dir = "../data/detections"

    detectron2_detection = Detectron2Detection(weights_file, detections_dir, detection_callback=notify_on_detection)

    gstreamer = CameraGStreamerPipeline()     
    DETECTION_INTERVAL = 120 

    try:
        gstreamer.open_pipeline()
        prev_frame_time = 0
        last_detection_time = time.time()

        while True:
            frame = gstreamer.read_frame()

            # Calculate FPS
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps_text = f"FPS: {int(fps)}"
            cv2.putText(frame, fps_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Perform detection at intervals
            current_time = time.time()
            if current_time - last_detection_time >= DETECTION_INTERVAL:
                print("Running detection...")
                img_counter = int(time.time())  # Use current time as image counter
                frame = detectron2_detection.process_frame(frame, img_counter)
                if frame is None:  # Exit if 'q' was pressed during fault detection
                    break
                last_detection_time = current_time

            # Display the live feed
            cv2.imshow("Detectron2 Detection", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        gstreamer.close_pipeline()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
