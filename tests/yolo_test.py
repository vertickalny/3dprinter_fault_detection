import os
import cv2
from src.detection.yolo_detection import YOLODetection

def run_yolo_detection():
    # Directories
    samples_dir = "../data/samples/tests"
    detections_dir = "../data/detections/yolo"
    os.makedirs(detections_dir, exist_ok=True)

    # YOLO configuration
    yolo_model_path = "../data/models/best2.pt"
    yolo_detection = YOLODetection(
        model_path=yolo_model_path,
        frames_dir=samples_dir,
        detections_dir=detections_dir
    )

    # Iterate over samples
    for sample in os.listdir(samples_dir):
        if sample.endswith(".jpg"):
            sample_path = os.path.join(samples_dir, sample)
            print(f"Processing {sample} with YOLO...")

            # Read the image
            frame = cv2.imread(sample_path)

            # Run YOLO detection
            yolo_detection.process_frame(frame, img_counter=0)

if __name__ == "__main__":
    print("Starting YOLO detection script...")
    run_yolo_detection()
    print("YOLO detection complete.")
