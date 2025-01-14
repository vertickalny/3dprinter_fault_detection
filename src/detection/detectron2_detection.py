import cv2
import time
import os
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

class Detectron2Detection:
    def __init__(self, cfg_file, weights_file, detections_dir, device="cpu", threshold=0.5,):
        self.cfg = self.setup_config(cfg_file, weights_file, threshold, device)
        self.predictor = DefaultPredictor(self.cfg)
        self.detections_dir = detections_dir
        os.makedirs(detections_dir, exist_ok=True)

    def setup_config(self, cfg_file, weights_file, threshold, device):
        cfg = get_cfg()
        cfg.merge_from_file(cfg_file)
        cfg.MODEL.WEIGHTS = weights_file
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        cfg.MODEL.DEVICE = device
        return cfg

    def process_frame(self, frame, img_counter):
        outputs = self.predictor(frame)
        instances = outputs["instances"].to("cpu")

        if len(instances) > 0:
            print("Detections found!")
            visualizer = Visualizer(
                frame[:, :, ::-1],
                MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
                scale=1.0
            )
            output = visualizer.draw_instance_predictions(instances)
            detection_frame = output.get_image()[:, :, ::-1]

            detection_path = os.path.join(self.detections_dir, f"detection_{img_counter}.jpg")
            cv2.imwrite(detection_path, detection_frame)
            print(f"Detection image saved to: {detection_path}")
            return detection_frame
        else:
            print("No detections found.")
            return frame

    def run(self, gst_pipeline, detection_interval=60):
        cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
        if not cap.isOpened():
            print("Error: Unable to open camera with GStreamer pipeline.")
            return

        prev_frame_time = 0
        last_detection_time = time.time()
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
                cv2.putText(frame, fps_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Perform detection at intervals
                current_time = time.time()
                if current_time - last_detection_time >= detection_interval:
                    print("Running detection...")
                    frame = self.process_frame(frame, img_counter)
                    img_counter += 1
                    last_detection_time = current_time

                # Display the live feed
                cv2.imshow("Detectron2 Detection", frame)

                # Exit on 'q' key press
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

    cfg_file = "../../configs/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
    weights_file = "../../data/models/model_final.pth"

    detectron2_detection = Detectron2Detection(cfg_file, weights_file, detections_dir="../../data/detections")
    detectron2_detection.run(gst_pipeline)
