from ultralytics import YOLO
import cv2
import time
import os

class YOLODetection:
    def __init__(self, model_path, frames_dir, detections_dir, conf_threshold=0.3 ):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.frames_dir = frames_dir
        self.detections_dir = detections_dir
        os.makedirs(frames_dir, exist_ok=True)
        os.makedirs(detections_dir, exist_ok=True)

    def process_frame(self, frame, img_counter):
        """Process a frame for detection and save results."""
        img_name = f'opencv_frame_{img_counter}.jpg'
        img_path = os.path.join(self.frames_dir, img_name)
        cv2.imwrite(img_path, frame)

        result = self.model(img_path, conf=self.conf_threshold)
        if len(result[0].boxes) > 0:
            print('Detection Happened')
            detection_img_path = os.path.join(self.detections_dir, f'result_of_{img_name}')

            # Draw detection boxes on the frame
            for box in result[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                class_index = int(box.cls[0])
                label_name = self.model.names[class_index]  # Get the label name from the model
                label = f"{label_name} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            # Save the modified frame with detections
            cv2.imwrite(detection_img_path, frame)
            return frame
        else:
            print("No Detection")
            if os.path.exists(img_path):
                os.remove(img_path)
            return frame

    def run(self, gst_pipeline, capture_interval=5):
        cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
        if not cap.isOpened():
            print("Error: Unable to open camera with GStreamer pipeline.")
            return

        prev_frame_time = 0
        img_counter = 0
        last_capture_time = time.time()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Unable to capture frame.")
                    break

                # Calculate FPS
                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time
                fps = int(fps)
                cv2.putText(frame, str(fps), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Process frames at intervals
                current_time = time.time()
                if current_time - last_capture_time >= capture_interval:
                    frame = self.process_frame(frame, img_counter)
                    img_counter += 1
                    last_capture_time = current_time

                # Display the frame
                cv2.imshow("YOLO Detection", frame)

                # Exit on 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    gst_pipeline = (
        "v4l2src device=/dev/video0 ! "
        "image/jpeg, width=640, height=480, framerate=30/1 ! "
        "jpegdec ! videoconvert ! appsink"
    )
    model_path = "../../data/models/best2.pt"

    yolo_detection = YOLODetection(model_path=model_path, frames_dir="../../data/frames", detections_dir="../../data/detections/")
    yolo_detection.run(gst_pipeline)
