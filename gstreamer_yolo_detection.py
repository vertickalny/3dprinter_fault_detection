import cv2
import time
import os
from ultralytics import YOLO

def main():
    # Load the YOLO model
    model = YOLO('best2.pt')
    conf_threshold = 0.3

    # Define the GStreamer pipeline
    gst_pipeline = (
        "v4l2src device=/dev/video0 ! "
        "image/jpeg, width=640, height=480, framerate=30/1 ! "
        "jpegdec ! videoconvert ! appsink"
    )

    # Open the video capture with GStreamer
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Unable to open camera with GStreamer pipeline.")
        return

    # Variables for FPS calculation
    prev_frame_time = 0
    new_frame_time = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Set up directories
    frames_dir = "frames"
    detections_dir = "detections"
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(detections_dir, exist_ok=True)

    # Frame capture interval and counter
    capture_interval = 5
    last_capture_time = time.time()
    img_counter = 0

    def process_frame(frame, img_counter):
        """Process a frame for detection and save results."""
        img_name = f'opencv_frame_{img_counter}.jpg'
        img_path = os.path.join(frames_dir, img_name)
        cv2.imwrite(img_path, frame)

        result = model(img_path, conf=conf_threshold)
        if len(result[0].boxes) > 0:
            print('Detection Happened')
            detection_img_path = os.path.join(detections_dir, f'result_of_{img_name}')

            # Draw detection boxes on the frame
            for box in result[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                class_index = int(box.cls[0])
                label_name = model.names[class_index]  # Get the label name from the model
                label = f"{label_name} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            # Save the modified frame with detections
            cv2.imwrite(detection_img_path, frame)
            return frame
        else:
            print("NO DETECTION")
            if os.path.exists(img_path):
                os.remove(img_path)
            return frame
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break

            # Calculate FPS
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            print("fps = ", fps)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)

            print("FPS: ", fps)
            cv2.putText(frame, fps, (10, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Process frames at intervals
            current_time = time.time()
            if current_time - last_capture_time >= capture_interval:
                frame = process_frame(frame, img_counter)
                img_counter += 1
                last_capture_time = current_time

            # Display the frame with or without detections
            cv2.imshow("Camera Capture with GStreamer", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
