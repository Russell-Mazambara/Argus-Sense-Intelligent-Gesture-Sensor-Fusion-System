"""
Argus Sense - Main Application Entry Point
Stage 3: Basic Gesture Recognition
"""

from hardware.arduino_interface import ArduinoReader
from vision.camera import CameraCapture
from vision.hand_tracker import HandTracker
from vision.gesture_recognizer import GestureRecognizer
import cv2
import time


def main():
    """
    Unified system with gesture recognition.
    
    Displays:
    - Live camera feed with hand tracking
    - Recognized gesture
    - Finger states visualization
    - Arduino sensor readings
    - FPS counter
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
    
    # Initialize gesture recognizer
    gesture_recognizer = GestureRecognizer()
    
    print("\n" + "=" * 60)
    print("✅ System Ready!")
    print("=" * 60)
    print("\nSupported Gestures:")
    print("  👊 FIST - All fingers closed")
    print("  ✋ OPEN_PALM - All fingers extended")
    print("  ☝️  POINTING - Index finger only")
    print("  ✌️  PEACE - Index and middle fingers")
    print("  👍 THUMBS_UP - Thumb only")
    print("\nControls:")
    print("  'q' - Quit")
    print("  ESC - Quit")
    print("\nShow gestures to the camera...")
    print()
    
    # FPS calculation
    prev_time = time.time()
    
    # Sensor data storage
    sensor_data = None
    waiting_for_first_read = arduino_connected
    
    # Current gesture
    current_gesture = None
    
    try:
        while True:
            # Read Arduino sensors (if connected)
            if arduino_connected:
                new_data = arduino.read_sensors()
                if new_data:
                    sensor_data = new_data
                    waiting_for_first_read = False
            
            # Read camera frame
            ret, frame = camera.read_frame()
            if not ret:
                print("⚠️  Failed to read frame")
                break
            
            # Process frame for hand tracking
            frame, hand_landmarks = tracker.process_frame(frame, draw=True)
            
            # Recognize gesture
            current_gesture = gesture_recognizer.recognize_gesture(hand_landmarks)
            
            # Get finger states for display
            finger_states = gesture_recognizer.get_finger_states(hand_landmarks)
            
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
            else:
                cv2.putText(frame, 'NO HAND', (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Gesture Recognition (center-left, large)
            if current_gesture and current_gesture != "UNKNOWN":
                # Background box for gesture
                cv2.rectangle(frame, (10, 120), (300, 200), (0, 0, 0), -1)
                
                # Gesture name (large text)
                cv2.putText(frame, f'GESTURE: {current_gesture}', (20, 160),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                
                # Finger states
                if finger_states:
                    finger_text = f"Fingers: {sum(finger_states.values())}/5"
                    cv2.putText(frame, finger_text, (20, 190),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Finger State Indicators (left side)
            if finger_states:
                y_offset = 220
                finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
                finger_keys = ['thumb', 'index', 'middle', 'ring', 'pinky']
                
                cv2.putText(frame, 'FINGER STATES:', (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                for i, (name, key) in enumerate(zip(finger_names, finger_keys)):
                    y_pos = y_offset + 25 + (i * 25)
                    status = "UP" if finger_states[key] else "DOWN"
                    color = (0, 255, 0) if finger_states[key] else (128, 128, 128)
                    
                    cv2.putText(frame, f'{name}: {status}', (10, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Arduino Sensor Data (top-right)
            if arduino_connected:
                cv2.rectangle(frame, (440, 10), (630, 120), (0, 0, 0), -1)
                
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
                    cv2.putText(frame, 'Waiting for Arduino...', (450, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # System Status (bottom)
            if current_gesture and current_gesture != "UNKNOWN":
                status_text = f"Gesture Recognized: {current_gesture}"
                color = (0, 255, 0)
            else:
                status_text = "Show a gesture (Fist, Open Palm, Point, Peace, Thumbs Up)"
                color = (255, 255, 255)
            
            cv2.putText(frame, status_text, (10, 460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
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