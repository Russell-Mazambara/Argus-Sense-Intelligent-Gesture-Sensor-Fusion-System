
from vision.camera import CameraCapture
import cv2

def main():
    
    print("Testing camera capture")
    camera=CameraCapture(camera_id=0)
    if not camera.open():
        print("❌ Camera failed to open")
        return
    
    print("Press 'q' to quit")
    
    while True:
        ret, frame=camera.read_frame()
        
        if not ret:
            break
        
        cv2.imshow("Camera Feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()