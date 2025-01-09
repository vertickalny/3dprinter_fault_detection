import cv2

# Define GStreamer pipeline to read from shared memory
gst_pipeline = (
    "shmsrc socket-path=/dev/shm/camera_feed ! videoconvert ! video/x-raw,format=BGR ! appsink"
)

# Open the pipeline as a video capture device
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to connect to the shared memory stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of stream or error.")
        break

    # Display the frame
    cv2.imshow("Shared Memory Frame", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

