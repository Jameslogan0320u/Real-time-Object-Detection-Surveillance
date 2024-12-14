// camera_setup.py 
import cv2 
def initialize_camera(): 
cap = cv2.VideoCapture(0) 
if not cap.isOpened(): 
print("Error: Could not open webcam.") 
exit() 
return cap 
def capture_frame(cap): 
ret, frame = cap.read() 
    if not ret: 
        print("Error: Failed to capture frame.") 
        return None 
    return frame 
 
if __name__ == "__main__": 
    cap = initialize_camera() 
    while True: 
        frame = capture_frame(cap) 
        if frame is None: 
            break 
        cv2.imshow("Camera Feed", frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break 
    cap.release() 
    cv2.destroyAllWindows()
