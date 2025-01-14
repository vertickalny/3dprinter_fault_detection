import subprocess
import cv2
import time
import os
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

def setup_detection(cfg_file, weights_file, threshold, device):
    """
    Sets up the Detectron2 configuration and predictor.
    """
    cfg = get_cfg()
    cfg.merge_from_file(cfg_file)
    cfg.MODEL.WEIGHTS = weights_file
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
    cfg.MODEL.DEVICE = device
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 80
    predictor = DefaultPredictor(cfg)
    return cfg, predictor

def perform_detection(frame, predictor, cfg, detections_dir, img_counter):
    """
    Performs object detection on the given frame and saves detection images.
    """
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

def test_detection_with_images(images_dir, cfg, predictor, detections_dir):
    """
    Test the detection model on a set of JPEG images in the specified directory.
    """
    os.makedirs(detections_dir, exist_ok=True)
    img_counter = 0

    for img_file in os.listdir(images_dir):
        if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
            img_path = os.path.join(images_dir, img_file)
            print(f"Processing image: {img_path}")

            frame = cv2.imread(img_path)
            if frame is None:
                print(f"Error: Unable to read image {img_path}")
                continue

            detection_happened = perform_detection(frame, predictor, cfg, detections_dir, img_counter)

            if detection_happened:
                img_counter += 1

def main():
    # Load the Detectron2 configuration
    cfg_file = "../configs/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
    weights_file = "../data/models/model_final.pth"
    threshold = 0.5
    device = "cpu"

    cfg, predictor = setup_detection(cfg_file, weights_file, threshold, device)

    # Path to the directory containing JPEG images
    images_dir = "../data/samples/tests"  # Current directory
    detections_dir = "./data/detections"

    print(f"Running detection on images in directory: {images_dir}")
    test_detection_with_images(images_dir, cfg, predictor, detections_dir)

    print("Detection completed on all images.")

if __name__ == "__main__":
    main()
