import os
import cv2
from src.detection.detectron2_detection import Detectron2Detection

def run_detectron2_detection():
    # Directories
    samples_dir = "../data/samples/tests"
    detections_dir = "../data/detections/detectron2"
    os.makedirs(detections_dir, exist_ok=True)

    # Detectron2 configuration
    detectron2_cfg_file = "../configs/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
    detectron2_weights_file = "../data/models/model_final.pth"
    detectron2_detection = Detectron2Detection(
        cfg_file=detectron2_cfg_file,
        weights_file=detectron2_weights_file,
        detections_dir=detections_dir
    )

    # Iterate over samples
    for sample in os.listdir(samples_dir):
        if sample.endswith(".jpg"):
            sample_path = os.path.join(samples_dir, sample)
            print(f"Processing {sample} with Detectron2...")

            # Read the image
            frame = cv2.imread(sample_path)

            # Run Detectron2 detection
            detectron2_detection.perform_detection(
                frame=frame,
                predictor=detectron2_detection.predictor,
                cfg=detectron2_detection.cfg,
                detections_dir=detections_dir,
                img_counter=0
            )

if __name__ == "__main__":
    print("Starting Detectron2 detection script...")
    run_detectron2_detection()
    print("Detectron2 detection complete.")
