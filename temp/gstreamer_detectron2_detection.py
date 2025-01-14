import cv2
import time
import os
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

def setup_detection(cfg_file, weights_file, threshold, device):
    cfg = get_cfg()
    cfg.merge_from_file(cfg_file)
    cfg.MODEL.WEIGHTS = weights_file
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
    cfg.MODEL.DEVICE = device
    predictor = DefaultPredictor(cfg)
    return cfg, predictor

def perform_detection(frame, predictor, cfg, detections_dir, img_counter):
    outputs = predictor(frame)
    instances = outputs["instances"].to("cpu")

    if len(instances) > 0:
        print("Detections found!")
        v = Visualizer(frame[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.0)
        out = v.draw_instance_predictions(instances)
        detection_frame = out.get_image()[:, :, ::-1]

        detection_path = os.path.join(detections_dir, f"detection_{img_counter}.jpg")
        cv2.imwrite(detection_path, detection_frame)
        print(f"Detection image saved to: {detection_path}")
        return True
    else:
        print("No detections found.")
        return False

def main():
    # Load the configuration
    cfg_file = "./configs/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
    weights_file = "./data/models/model_final.pth"
    threshold = 0.5
    device = "cpu"

    cfg, predictor = setup_detection(cfg_file, weights_file, threshold, device)

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

    # Variables for FPS calculation and timing
    prev_frame_time = 0
    detection_interval = 60# seconds
    last_detection_time = time.time()

    # Set up directories
    detections_dir = "./data/detections"
    os.makedirs(detections_dir, exist_ok=True)

    img_counter = 0

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
            fps_text = f"FPS: {int(fps)}"
            print(fps_text)

            # Display FPS on the frame
            cv2.putText(frame, fps_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Perform detection every `detection_interval` seconds
            current_time = time.time()
            if current_time - last_detection_time >= detection_interval:
                print("Running detection...")
                detection_happened = perform_detection(frame, predictor, cfg, detections_dir, img_counter)

                if detection_happened:
                    img_counter += 1

                last_detection_time = current_time

            # Display the live feed
            cv2.imshow("Detectron2 Detection", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

