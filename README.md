---

```markdown
# 3D Printer Fault Detection for SpaceVela

This project is part of the **SpaceVela** initiative, designed to detect anomalies in 3D printer operations by analyzing captured images using AI-based object detection models, including YOLO and Detectron2. The system processes images(taken from a camera) and provides annotated outputs highlighting detected faults.

---

## Repository Structure

```plaintext
3dprinter_fault_detection/
├── data/
│   ├── models/                 # Pre-trained models
│   │   ├── best2.pt            # YOLO model
│   │   └── model_final.pth     # Detectron2 model
│   ├── samples/                # Input samples
│   │   └── tests/              # Test images with defects
├── examples/
│   ├── run_yolo_detection.py   # YOLO example script
│   ├── run_detectron2_detection.py # Detectron2 example script
├── scripts/
│   ├── install_gstreamer.sh    # GStreamer installation script
│   ├── build_opencv_with_gstreamer.sh # Build OpenCV with GStreamer
│   ├── README.md               # Detailed OpenCV build instructions
├── tests/                      # Test suite for modules
├── src/                        # Application source code
│   ├── camera.py               # Camera handling module
│   ├── detection/
│   │   ├── yolo_detection.py   # YOLO detection module
│   │   └── detectron2_detection.py  # Detectron2 detection module
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
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

### **Key Updates**
1. **OpenCV Build Reference**: Added a link to `/scripts/README.md` for detailed OpenCV build instructions.
2. **Repository Structure**: Matches your actual repository layout.
3. **Streamlined Installation**: Clearly guides users on prerequisites and setup steps.

Let me know if further changes are needed!
