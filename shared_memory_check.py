
import os
import mmap
import cv2
import numpy as np
import time

# Shared memory path and video properties
shm_path = "/dev/shm/camera_feed"
frame_width = 640
frame_height = 480
frame_format = "BGR"  # Matches GStreamer format
frame_size = frame_width * frame_height * 3  # Width x Height x Channels

def read_shared_memory(shm_path, frame_size):
    """
    Reads a frame from shared memory.
    """
    try:
        # Open the shared memory file in read-only mode
        with open(shm_path, "rb") as shm_file:
            with mmap.mmap(shm_file.fileno(), frame_size, access=mmap.ACCESS_READ) as shm:
                # Read raw frame data from shared memory
                frame_data = shm.read(frame_size)
                shm.seek(0)  # Reset pointer for next read
                return frame_data
    except Exception as e:
        print(f"Error accessing shared memory: {e}")
        return None

def main():
    print("Press 'q' to quit.")
    
    # Check if shared memory exists
    if not os.path.exists(shm_path):
        print(f"Shared memory file {shm_path} does not exist!")
        return

    while True:
        # Read frame data from shared memory
        frame_data = read_shared_memory(shm_path, frame_size)
        if frame_data is None:
            time.sleep(0.1)  # Wait before retrying
            continue

        try:
            # Convert raw data to NumPy array and reshape to frame dimensions
            frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((frame_height, frame_width, 3))

            # Display the frame using OpenCV
            cv2.imshow("Shared Memory Video Feed", frame)
        except Exception as e:
            print(f"Error processing frame: {e}")
            continue

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

