"""Diagnostic test to identify LED pin mapping"""

from hardware.arduino_interface import ArduinoReader
import time

def main():
    print("🔍 LED PIN DIAGNOSTIC TEST")
    print("=" * 50)
    print("This will test each Arduino pin individually")
    print("to identify which color each pin controls.\n")
    
    arduino = ArduinoReader('COM4') 
    
    if not arduino.connect():
        print("Failed to connect!")
        return
    
    # Turn off LED first
    arduino.set_led(0, 0, 0)
    time.sleep(1)
    
    print("\n" + "=" * 50)
    print("TEST 1: Testing RED channel (Pin 5)")
    print("=" * 50)
    arduino.set_led(255, 0, 0)  # Only red channel ON
    color = input("What COLOR do you see? (type the color): ").strip().lower()
    print(f"Pin 5 (redPin) controls: {color.upper()}")
    
    arduino.set_led(0, 0, 0)
    time.sleep(1)
    
    print("\n" + "=" * 50)
    print("TEST 2: Testing GREEN channel (Pin 6)")
    print("=" * 50)
    arduino.set_led(0, 255, 0)  # Only green channel ON
    color = input("What COLOR do you see? (type the color): ").strip().lower()
    print(f"Pin 6 (greenPin) controls: {color.upper()}")
    
    arduino.set_led(0, 0, 0)
    time.sleep(1)
    
    print("\n" + "=" * 50)
    print("TEST 3: Testing BLUE channel (Pin 3)")
    print("=" * 50)
    arduino.set_led(0, 0, 255)  # Only blue channel ON
    color = input("What COLOR do you see? (type the color): ").strip().lower()
    print(f"Pin 3 (bluePin) controls: {color.upper()}")
    
    # Turn off
    arduino.set_led(0, 0, 0)
    
    print("\n" + "=" * 50)
    print("DIAGNOSTIC SUMMARY:")
    print("=" * 50)
    print("Now tell me what you saw for each test!")
    
    arduino.disconnect()

if __name__ == "__main__":
    main()