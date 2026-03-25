"""
Arduino Serial Interface Module

Handles real-time communication with Arduino sensors via serial port.
Provides validated sensor data in structured dictionary format.
"""



import serial
import time
from typing import Optional, Dict

class ArduinoReader:
    """
    Interface for reading sensor data from Arduino via serial communication.
    
    Attributes:
        port (str): Serial port identifier (e.g., 'COM3', '/dev/ttyUSB0')
        baudrate (int): Communication speed (must match Arduino)
        timeout (float): Serial read timeout in seconds
    """
    def disconnect(self) -> None:  
        """Close serial connection cleanly."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self._is_connected = False
            print("✅ Disconnected from Arduino")

    def is_connected(self) -> bool:
         """Check if currently connected to Arduino."""
         return self._is_connected

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.disconnect()
    def __init__(self, port: str, baudrate: int=9600, timeout: float=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection=None
        self._is_connected=False
        
    def connect(self)->bool:
        """
        Establish serial connection with Arduino.
        
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)
            self.serial_connection.reset_input_buffer()
            self._is_connected=True
            print(f"✅ Connected to Arduino on {self.port}")
            return True
        except serial.SerialException as e:
             print(f"❌ Failed to connect to {self.port}: {e}")
             self._is_connected = False
             return False
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            self._is_connected = False
            return False
            
    def _parse_data(self, data_string: str) -> Optional[Dict[str, int]]:
        """ 
        Parse Arduino data string into dictionary.
        
        Args:
        data_string: String like "US:45,L1:512,L2:380"
        
        Returns:
        Dictionary like {'ultrasonic': 45, 'light1': 512, 'light2': 380}
        or None if parsing fails
        
        """
        try:
            parts=data_string.split(",")
            
            data={}
            key_map={
                'US': 'ultrasonic',
                'L1': 'light1',
                'L2': 'light2'
            }
            
            for part in parts:
                key, value = part.split(":")
                value=int(value)
                friendly_key = key_map[key]
                data[friendly_key] = value
            return data
        except (ValueError, KeyError, IndexError) as e:
            print(f"⚠️  Parse error: {data_string} - {e}")
            return None
        
    def read_sensors(self)->Optional[Dict[str, int]]:
        """
        Read one sensor data packet from Arduino.
    
        Returns:
        Dictionary with sensor values or None if read fails
        """
        if not self._is_connected:
           
            return None
        try:
            if self.serial_connection.in_waiting > 0:
                raw_data= self.serial_connection.readline()
                data_string=raw_data.decode('utf-8').strip()
                return self._parse_data(data_string)
            else:
                return None
        except serial.SerialException as e:
            print(f"❌ An error occurred: {e}")
            self._is_connected = False
            return None
        
        except UnicodeDecodeError as e:
            print(f"❌ An error occurred: {e}")
            return None
        
       
            
            