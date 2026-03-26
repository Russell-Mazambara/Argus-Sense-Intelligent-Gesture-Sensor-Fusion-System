"""Test hand tracking with camera"""

from vision.camera import CameraCapture
from vision.hand_tracker import HandTracker
import cv2
import time


def main():
    print("🖐️  Testing hand tracking...")
    print("Show your hand to the camera")
    print("Press 'q' to quit")
    
    # Initialize camera and tracker
    camera = CameraCapture()
    tracker = HandTracker()
    
    if not camera.open():
        print("Failed to open camera!")
        return
    
    # FPS calculation
    prev_time = time.time()
    
    while True:
        # Read frame
        ret, frame = camera.read_frame()
        if not ret:
            break
        
        # Process frame for hand tracking
        frame, hand_landmarks = tracker.process_frame(frame, draw=True)
        
        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Display FPS
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display hand detection status
        if hand_landmarks:
            cv2.putText(frame, 'Hand Detected!', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Hand Tracking Test', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    camera.release()
    tracker.close()
    cv2.destroyAllWindows()
    print("✅ Test complete!")


if __name__ == "__main__":
    main()