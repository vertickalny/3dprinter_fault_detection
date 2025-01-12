import cv2
import time

def main():
    # Open the camera
    camera = cv2.VideoCapture(0)
    
    prev_frame_time = 0
    new_frame_time = 0
    font = cv2.FONT_HERSHEY_SIMPLEX 
    
    if not camera.isOpened():
        print("Error: Cannot access the camera.")
        return
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # Variables for FPS calculation
    frame_count = 0
    start_time = time.time()

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab frame")
                break

            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            cv2.putText(frame, fps, (7,70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
           # Display the frame
            cv2.imshow('Raspberry Pi Camera', frame)
            
            # Exit the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

