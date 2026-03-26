"""
Argus Sense - Main Application Entry Point
Stage 2: Computer Vision + Hardware Integration
"""

from hardware.arduino_interface import ArduinoReader
from vision.camera import CameraCapture
from vision.hand_tracker import HandTracker
import cv2
import time


def main():
    """
    Unified system combining Arduino sensors and computer vision.
    
    Displays:
    - Live camera feed with hand tracking
    - Arduino sensor readings overlaid on video
    - FPS counter
    - System status
    """
    
    # Configuration
    ARDUINO_PORT = 'COM4'  # ⚠️ Update to your port!
    
    print("=" * 60)
    print("🚀 ARGUS SENSE - Intelligent Gesture Control System")
    print("=" * 60)
    print("\nInitializing systems...")
    
    # Initialize Arduino
    arduino = ArduinoReader(port=ARDUINO_PORT, baudrate=9600)
    arduino_connected = arduino.connect()
    
    if not arduino_connected:
        print("⚠️  Continuing without Arduino (vision-only mode)")
    
    # Initialize camera
    camera = CameraCapture(width=640, height=480)
    if not camera.open():
        print("❌ Failed to open camera. Exiting.")
        return
    
    # Initialize hand tracker
    tracker = HandTracker(
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.5
    )
    
    print("\n" + "=" * 60)
    print("✅ System Ready!")
    print("=" * 60)
    print("\nControls:")
    print("  'q' - Quit")
    print("  ESC - Quit")
    print("\nShow your hand to the camera...")
    print()
    
    # FPS calculation
    prev_time = time.time()
    
    # Sensor data storage - PERSIST LAST VALID READING
    sensor_data = None
    waiting_for_first_read = arduino_connected  # Track if we've gotten first reading
    
    try:
        while True:
            # Read Arduino sensors (if connected)
            if arduino_connected:
                new_data = arduino.read_sensors()  # Get new data
                if new_data:  # Only update if we got valid data
                    sensor_data = new_data
                    waiting_for_first_read = False  # We've gotten at least one reading
            
            # Read camera frame
            ret, frame = camera.read_frame()
            if not ret:
                print("⚠️  Failed to read frame")
                break
            
            # Process frame for hand tracking
            frame, hand_landmarks = tracker.process_frame(frame, draw=True)
            
            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            
            # ========================================
            # OVERLAY INFORMATION ON FRAME
            # ========================================
            
            # FPS Counter (top-left)
            cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Hand Detection Status
            if hand_landmarks:
                cv2.putText(frame, 'HAND DETECTED', (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Count landmarks for verification
                num_hands = len(hand_landmarks)
                cv2.putText(frame, f'Hands: {num_hands}', (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'NO HAND', (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Arduino Sensor Data (top-right)
            # Always draw the background box if Arduino is connected
            if arduino_connected:
                # Background box for sensor data
                cv2.rectangle(frame, (440, 10), (630, 120), (0, 0, 0), -1)
                
                # Display data if we have it
                if sensor_data:
                    cv2.putText(frame, 'ARDUINO SENSORS', (450, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, f'Distance: {sensor_data["ultrasonic"]}cm', (450, 55),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, f'Light1: {sensor_data["light1"]}', (450, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, f'Light2: {sensor_data["light2"]}', (450, 105),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                elif waiting_for_first_read:
                    # Only show "waiting" if we haven't gotten ANY data yet
                    cv2.putText(frame, 'Waiting for Arduino...', (450, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            else:
                # Arduino disconnected - show status
                cv2.putText(frame, 'Arduino: Disconnected', (450, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            
            # System Status (bottom)
            status_text = "READY - Show hand for tracking"
            cv2.putText(frame, status_text, (10, 460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('Argus Sense - Gesture Control System', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    
    finally:
        # Cleanup
        print("\n🔄 Shutting down systems...")
        
        if arduino_connected:
            arduino.disconnect()
        
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()
        
        print("✅ Shutdown complete!")
        print("\n👋 Goodbye!\n")


if __name__ == "__main__":
    main()