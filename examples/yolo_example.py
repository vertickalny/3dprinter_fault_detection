# Example usage for YOLODetection
# first in command line, type export PYTHONPATH=$(pwd)/..
from src.detection.yolo_detection import YOLODetection

def run_yolo_example():
    gst_pipeline = (
        "v4l2src device=/dev/video0 ! "
        "image/jpeg, width=640, height=480, framerate=30/1 ! "
        "jpegdec ! videoconvert ! appsink"
    )

    model_path = "../data/models/best2.pt"
    frames_dir = "../data/frames"
    detections_dir = "../data/detections"

    yolo_detection = YOLODetection(
        model_path=model_path,
        frames_dir=frames_dir,
        detections_dir=detections_dir
    )

    yolo_detection.run(gst_pipeline, capture_interval=5)

if __name__ == "__main__":
    print("Running YOLO Detection Example...")
    run_yolo_example()

