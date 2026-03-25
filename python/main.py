"""
Argus Sense - Main Application Entry Point
Stage 1B: Testing Arduino Serial Communication
"""

from hardware.arduino_interface import ArduinoReader
import time

def main():
    """Testing Arduino serial communication"""
    
    Arduino_Port='COM4'
    
    print("🏃‍♀️ Starting Argus Sense...")
    print("="*50)
    
    Reader= ArduinoReader(port=Arduino_Port,baudrate=9600,timeout=1.0)
    
    if not Reader.connect():
        print("❌ Failed to connect to Arduino. Check port and try again")
        return
    
    print("✅ Connected to Arduino")
    print("="*50)
    
    try:
        read_count=0
        successful_reads=0
        
        while True:
            data=Reader.read_sensors()
            
            if data:
                successful_reads+=1
                print(f"Reading#{successful_reads:03d}|"
                      f"Distance: {data['ultrasonic']}cm|"
                      f"Light1: {data['light1']:4d}|"
                      f"Light2: {data['light2']:4d}"
                      )
                
            read_count+=1
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Stopped by user")
        print(f"Statistics:")
        print(f"Reads: {read_count}")
        print(f"Successful reads: {successful_reads}")
        print(f"Success rate: {successful_reads/read_count*100}%")
        
    finally:
        Reader.disconnect()
        print("="*50)
        print("🏃‍♀️ Argus Sense stopped")
        print("="*50)
        
        
if __name__ == "__main__":
    main()