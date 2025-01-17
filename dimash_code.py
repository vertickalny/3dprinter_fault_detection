import os
from detectron2.utils.visualizer import Visualizer
import cv2
from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
from detectron2.config import get_cfg
from detectron2 import model_zoo

# Inference Configuration
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = "./data/models/model_final.pth"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.DEVICE = "cpu"  # Use "cpu" for inference without GPU
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
MetadataCatalog.get("custom_metadata").set(thing_classes=["fail"])

# Initialize the predictor
predictor = DefaultPredictor(cfg)

# Path to the folder with test images
test_images_folder = "./data/samples/tests/"

# Iterate through each image in the folder
for image_filename in os.listdir(test_images_folder):
    image_path = os.path.join(test_images_folder, image_filename)

    # Read the image
    im = cv2.imread(image_path)

    # Skip invalid files
    if im is None:
        print(f"Could not read {image_path}, skipping...")
        continue

    # Print when detection starts
    print(f"Starting detection for {image_filename}...")

    # Run inference
    outputs = predictor(im)

    # Check if detections are found
    instances = outputs["instances"].to("cpu")
    if len(instances) > 0:
        print(f"Detections found for {image_filename}. Number of detections: {len(instances)}.")
    else:
        print(f"No detections found for {image_filename}.")

    # Print when detection ends
    print(f"Detection completed for {image_filename}.")

    # Visualize the predictions
    v = Visualizer(im[:, :, ::-1],
                   metadata=MetadataCatalog.get('custom_metadata'),  # Set metadata if available
                   scale=0.5)
    out = v.draw_instance_predictions(instances)

    # Display the image with predictions
    cv2.imshow("Predictions", out.get_image()[:, :, ::-1])

    # Wait for user to close the window or press a key
    key = cv2.waitKey(0)  # Wait indefinitely for a key press
    if key == ord('q'):  # Press 'q' to exit the loop early
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
