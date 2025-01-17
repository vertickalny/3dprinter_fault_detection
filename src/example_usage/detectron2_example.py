from detection.detectron2_detection import Detectron2Detection 
from utils.camera_gstreamer_module import CameraGStreamerPipeline
import cv2
import time

def main():
    weights_file = "../data/models/model_final.pth"
    detections_dir = "../data/detections"

    detectron2_detection = Detectron2Detection(weights_file, detections_dir)

    gstreamer = CameraGStreamerPipeline()     

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
            if current_time - last_detection_time >= 20:
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
