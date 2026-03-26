"""
Camera Capture Module

Handles webcam access and frame capture for computer vision pipeline.
"""

import cv2
from typing import Optional,Tuple
import numpy as np

class CameraCapture:
    """
    Manages webcam capture for real-time video processing.
    
     Attributes:
        camera_id (int): Camera index (0 = default camera)
        width (int): Frame width in pixels
        height (int): Frame height in pixels
    
    """
    def __init__(self, camera_id: int = 0, width: int = 640, height: int = 480):
        """
        Initialize camera capture.
        
        Args:
            camera_id: Camera index (0 for default, 1 for external USB camera)
            width: Desired frame width
            height: Desired frame height
        """
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap=None
        self._is_opened=False
        
    def open(self)->bool:
        """
        Open the camera for capturing frames.
        
        Returns:
            bool: True if successful, False otherwise
        """
            
        try:
            self.cap=cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                return False
            
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self._is_opened=True
            print(f"✅ Camera successfully opened on {self.camera_id}")
            return True
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            return False
            
    def read_frame(self)->Tuple[bool,np.ndarray]:
        """
        Read a frame from the camera.
        Returns:
        Tuple of (success, frame)
        - success: True if frame was read successfully
        - frame: NumPy array containing the image (BGR format)
        """
        
        if not self._is_opened:
            return False, None
        
        ret, frame = self.cap.read()
        return ret, frame
    
    def release(self)->None:
        """
        Release the camera resources.
        """
        if self._is_opened:
            self.cap.release()
            self._is_opened=False
            print(f"✅ Camera successfully released")
            
    def is_opened(self)->bool:
        """Check if camera is currently open."""
        return self._is_opened
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.release()