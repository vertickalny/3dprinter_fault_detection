import cv2

def main():
    # Open the camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Cannot access the camera.")
        return

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab frame")
                break
            
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
