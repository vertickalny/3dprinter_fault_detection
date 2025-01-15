
# OpenCV-Python Installation with GStreamer Support

This guide provides instructions to install OpenCV-Python with GStreamer support on **Raspberry Pi 5 Model B Rev 1.0**. Follow the steps below to set up the environment.

---

## Directory Structure
```plaintext
scripts/
│
├── GStreamer_CLI_shm_example.sh    # Example script demonstrating GStreamer CLI usage
├── gstreamer_install.sh            # Script to install GStreamer dependencies
├── install_opencv_dependencies.sh  # Script to install OpenCV build dependencies
└── ReadMe.md                       # This guide
```

---

## System Compatibility

This installation process is tailored for the following hardware:

**Model**: Raspberry Pi 5 Model B Rev 1.0  
**Operating System**: Raspberry Pi OS (or other compatible Debian-based distributions)

---

## Prerequisites

Ensure the following are installed on your system before proceeding:
- Python 3.x
- `pip` and `virtualenv`
- `git`

**Note**: Make sure you are working within a Python virtual environment to avoid conflicts with system-wide packages. To create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Installation Steps

### Step 1: Install GStreamer Dependencies

Run the `gstreamer_install.sh` script to install the necessary GStreamer libraries and plugins:
```bash
sudo chmod +x gstreamer_install.sh
./gstreamer_install.sh
```

This script installs a comprehensive set of GStreamer components, including OpenGL and OpenCV integrations.

---

### Step 2: Install OpenCV Dependencies

Run the `install_opencv_dependencies.sh` script to install the required dependencies for building OpenCV:
```bash
sudo chmod +x install_opencv_dependencies.sh
./install_opencv_dependencies.sh
```

---

### Step 3: GStreamer CLI Example

An example script `GStreamer_CLI_shm_example.sh` is provided to demonstrate GStreamer usage via the command line. To run the script:
```bash
sudo chmod +x GStreamer_CLI_shm_example.sh
./GStreamer_CLI_shm_example.sh
```

This example showcases how to use GStreamer for shared memory (SHM) video streaming.

---

## Verification

To verify the OpenCV installation:
1. Open a Python shell.
2. Run the following code:
```python
import cv2
print(cv2.getBuildInformation())
```
3. Ensure GStreamer support is enabled in the output.

---

## Troubleshooting

- Ensure all prerequisites are installed.
- Clean the build directory if re-installing:
  ```bash
  rm -rf /tmp/opencv_build
  ```

---

## Notes

This process has been tested specifically on the **Raspberry Pi 5 Model B Rev 1.0**. Compatibility with other hardware or operating systems may require adjustments.

---

## License

This project is distributed under the MIT License.

