---


# 3D Printer Fault Detection for SpaceVela

This project is part of the **SpaceVela** initiative, designed to detect anomalies in 3D printer operations by analyzing captured images using AI-based object detection models, including YOLO and Detectron2. The system processes images(taken from a camera) and provides annotated outputs highlighting detected faults.

---

## Repository Structure

```plaintext
3dprinter_camera_capture/
├── chatbot/                    # Chatbot for fault notifications
│   └── bot.py                 # Entry point for chatbot
├── configs/                    # Configuration files for models
│   ├── mask_rcnn_X_101_32x8d_FPN_3x.yaml
│   └── Base-RCNN-FPN.yaml
├── data/                       # Data directory
│   ├── models/                 # Pre-trained models
│   │   ├── best2.pt            # YOLO model
│   │   └── model_final.pth     # Detectron2 model
│   └── detections/             # Detected fault images (dynamic)
├── scripts/                    # Utility scripts
│   ├── gstreamer_install.sh    # GStreamer installation script
│   ├── install_opencv_dependencies.sh # OpenCV dependency installation
│   └── README.md               # OpenCv-Python with Gstreamer installation 
├── src/                        # Application source code
│   ├── detection/              # Detection modules
│   │   ├── yolo_detection.py
│   │   └── detectron2_detection.py
│   ├── klippy_api/             # Klippy API integration
│   │   └── KlippyAPI.py
│   ├── example_usage/          # Usage examples
│   │   ├── detectron2_example.py
│   │   └── yolo_example.py
│   ├── utils/                  # Utility modules
│   │   ├── camera_gstreamer_module.py
│   │   └── gstreamer_youtube_stream_test_example.py
│   └── main.py                 # Main script
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
```

---

## Prerequisites

1. **Hardware**: Raspberry Pi 5 Model B Rev 1.0 or equivalent.
2. **Software**:
   - Python 3.x
   - GStreamer libraries
   - OpenCV built with GStreamer support
   - Pre-trained YOLO and Detectron2 models

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/abay-kulamkadyr/3dprinter_fault_detection.git
cd 3dprinter_fault_detection
```

### Step 2: Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Install GStreamer Dependencies
Run the GStreamer installation script:
```bash
./scripts/install_gstreamer.sh
```

### Step 4: Build OpenCV with GStreamer Support
Refer to the [OpenCV Build Guide](scripts/README.md) for detailed instructions on how to build OpenCV with GStreamer support. Once complete, ensure OpenCV is correctly installed in your Python environment.

---

## Usage

### **Run YOLO Detection**
To process images using YOLO:
```bash
python3 examples/run_yolo_detection.py
```

### **Run Detectron2 Detection**
To process images using Detectron2:
```bash
python3 examples/run_detectron2_detection.py
```

### **Input and Output**
- **Input**: Place images to be processed in the `data/frames/` directory.
- **Output**: Detection results are saved in `data/detections/` with annotated images.

---

## Configuration

### **Models**
- Place YOLO and Detectron2 models in the `data/models/` directory.

### **GStreamer Pipeline**
Customize the GStreamer pipeline in scripts as needed. Example pipeline:
```python
gst_pipeline = (
    "v4l2src device=/dev/video0 ! "
    "image/jpeg, width=640, height=480, framerate=30/1 ! "
    "jpegdec ! videoconvert ! appsink"
)
```

### **Input Images For Testing**
- Save input images for processing in `data/samples/tests`.

---

## Testing

To validate the detection modules, run the test suite:
```bash
python3 -m unittest discover tests
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Developed by **Abay Kulamkadyr** for the **SpaceVela Project**.

```

---

