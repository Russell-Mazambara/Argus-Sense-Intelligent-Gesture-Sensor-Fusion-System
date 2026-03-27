"""Test LED control"""

from hardware.arduino_interface import ArduinoReader
import time

def main():
    print("🔴 Testing LED control...")
    
    arduino = ArduinoReader('COM4')  # Update port!
    
    if not arduino.connect():
        print("Failed to connect!")
        return
    
    print("Cycling through colors...")
    
    # Red
    print("Red...")
    arduino.set_led(255, 0, 0)
    time.sleep(2)
    
    # Green
    print("Green...")
    arduino.set_led(0, 255, 0)
    time.sleep(2)
    
    # Blue
    print("Blue...")
    arduino.set_led(0, 0, 255)
    time.sleep(2)
    
    # Yellow
    print("Yellow...")
    arduino.set_led(255, 255, 0)
    time.sleep(2)
    
    # Off
    print("Off...")
    arduino.set_led(0, 0, 0)
    
    arduino.disconnect()
    print("✅ Test complete!")

if __name__ == "__main__":
    main()