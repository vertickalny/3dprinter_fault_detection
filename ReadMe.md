3dprinter_fault_detection/
├── src/                        # Application source code
│   ├── __init__.py             # Indicates src is a package
│   ├── detection/
│   │   ├── __init__.py
│   │   ├── detectron2.py       # Detectron2 detection implementation
│   │   └── yolo.py             # YOLO detection implementation

├── tests/                      # Test suite
├── scripts/                    # Auxiliary scripts
│   ├── install_gstreamer.sh    # GStreamer installation script
│   └── install_opencv.sh       # OpenCV installation script
├── configs/                    # Configuration files
│   ├── detectron2_config.yaml
│   └── yolo_config.yaml
├── data/                       # Data files (e.g., models, datasets)
│   ├── models/
│   │   ├── detectron2_model.pth
│   │   └── yolo_model.pth
│   └── samples/
├── docs/                       # Documentation
│   └── setup_guide.md
├── .gitignore                  # Git ignore file
├── README.md                   # Project overview
└── requirements.txt      
