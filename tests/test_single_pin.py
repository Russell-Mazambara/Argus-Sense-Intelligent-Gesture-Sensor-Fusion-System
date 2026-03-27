"""Test each Arduino pin individually to find LED mapping"""

from hardware.arduino_interface import ArduinoReader
import time

def test_single_pin(arduino, pin_name, r, g, b):
    """Test a single pin by turning only it ON"""
    print(f"\n{'='*50}")
    print(f"Testing: {pin_name}")
    print(f"Sending: R={r}, G={g}, B={b}")
    print(f"{'='*50}")
    
    # Turn OFF first
    arduino.set_led(0, 0, 0)
    time.sleep(0.5)
    
    # Turn ON target pin
    arduino.set_led(r, g, b)
    time.sleep(0.5)
    
    color = input("What SINGLE pure color do you see (red/green/blue/none/multiple)? ").strip().lower()
    
    # Turn OFF
    arduino.set_led(0, 0, 0)
    time.sleep(0.5)
    
    return color

def main():
    print("🔍 SINGLE PIN LED MAPPING TEST")
    print("=" * 50)
    print("We'll test each Arduino pin ONE AT A TIME")
    print("to see which LED color it controls.\n")
    
    arduino = ArduinoReader('COM4')
    
    if not arduino.connect():
        print("Failed to connect!")
        return
    
    time.sleep(2)  # Wait for Arduino to stabilize
    
    # Test each pin individually
    results = {}
    
    # Test Pin 5 (defined as redPin)
    results['Pin 5 (redPin)'] = test_single_pin(arduino, "Pin 5 (redPin)", 255, 0, 0)
    
    # Test Pin 6 (defined as greenPin)
    results['Pin 6 (greenPin)'] = test_single_pin(arduino, "Pin 6 (greenPin)", 0, 255, 0)
    
    # Test Pin 3 (defined as bluePin)
    results['Pin 3 (bluePin)'] = test_single_pin(arduino, "Pin 3 (bluePin)", 0, 0, 255)
    
    # Summary
    print("\n" + "=" * 50)
    print("MAPPING RESULTS:")
    print("=" * 50)
    for pin, color in results.items():
        print(f"{pin} controls LED: {color.upper()}")
    
    print("\n" + "=" * 50)
    print("RECOMMENDED FIX:")
    print("=" * 50)
    
    # Determine correct mapping
    pin_to_color = {
        'Pin 5 (redPin)': results['Pin 5 (redPin)'],
        'Pin 6 (greenPin)': results['Pin 6 (greenPin)'],
        'Pin 3 (bluePin)': results['Pin 3 (bluePin)']
    }
    
    # Find which pin controls which color
    red_pin = None
    green_pin = None
    blue_pin = None
    
    for pin, color in pin_to_color.items():
        if 'red' in color:
            red_pin = pin.split()[1]  # Extract pin number
        elif 'green' in color:
            green_pin = pin.split()[1]
        elif 'blue' in color:
            blue_pin = pin.split()[1]
    
    if red_pin and green_pin and blue_pin:
        print(f"\nUpdate your Arduino code:")
        print(f"const int redPin = {red_pin};")
        print(f"const int greenPin = {green_pin};")
        print(f"const int bluePin = {blue_pin};")
    else:
        print("\nMultiple colors detected per pin - possible wiring issue!")
        print("Check your connections.")
    
    arduino.disconnect()

if __name__ == "__main__":
    main()