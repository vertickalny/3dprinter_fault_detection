# first in command line, type export PYTHONPATH=$(pwd)/..
from src.detection.detectron2_detection import Detectron2Detection

def run_detectron2_example():
    gst_pipeline = (
        "v4l2src device=/dev/video0 ! "
        "image/jpeg, width=640, height=480, framerate=30/1 ! "
        "jpegdec ! videoconvert ! appsink"
    )

    cfg_file = "../configs/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
    
    weights_file = "../data/models/model_final.pth"
    detections_dir = "../data/detections"

    detectron2_detection = Detectron2Detection(
        cfg_file=cfg_file,
        weights_file=weights_file,
        detections_dir=detections_dir
    )

    detectron2_detection.run(gst_pipeline, detection_interval=60)

if __name__ == "__main__":
    print("Running Detectron2 Detection Example...")
    run_detectron2_example()
