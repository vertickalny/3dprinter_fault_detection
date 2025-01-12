import cv2
import time

def main():
    # Define the GStreamer pipeline
    gst_pipeline = (
         "v4l2src device=/dev/video0 ! "
        "image/jpeg, width=1920, height=1080, framerate=30/1 ! "
        "jpegdec ! videoconvert ! appsink"
    )

    # Open the video capture with GStreamer
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Unable to open camera with GStreamer pipeline.")
        return

    # Variables for FPS calculation
    prev_frame_time = 0
    new_frame_time = 0
    font = cv2.FONT_HERSHEY_SIMPLEX 
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break

            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            cv2.putText(frame, fps, (7,70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            # Display the frame
            cv2.imshow("Camera Capture with GStreamer", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

