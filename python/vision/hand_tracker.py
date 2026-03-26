"""
Hand Tracking Module

Uses MediaPipe to detect and track hand landmarks in real-time.
"""

import cv2
import mediapipe as mp
from typing import Optional, List, Tuple
import numpy as np


class HandTracker:
    """
    Real-time hand detection and landmark tracking using MediaPipe.
    
    Attributes:
        max_hands (int): Maximum number of hands to detect
        detection_confidence (float): Minimum confidence for detection (0.0-1.0)
        tracking_confidence (float): Minimum confidence for tracking (0.0-1.0)
    """
    
    def __init__(
        self,
        max_hands: int = 1,
        detection_confidence: float = 0.8,
        tracking_confidence: float = 0.9
    ):
        """
        Initialize MediaPipe hand tracking.
        
        Args:
            max_hands: Maximum number of hands to detect (1 or 2)
            detection_confidence: Minimum detection confidence (higher = stricter)
            tracking_confidence: Minimum tracking confidence (higher = stricter)
        """
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        
        # Initialize drawing utilities
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_styles = mp.solutions.drawing_styles
    
    def process_frame(
        self,
        frame: np.ndarray,
        draw: bool = True
    ) -> Tuple[np.ndarray, Optional[List]]:
        """
        Process frame to detect hands and optionally draw landmarks.
        
        Args:
            frame: Input image (BGR format from OpenCV)
            draw: Whether to draw landmarks on the frame
            
        Returns:
            Tuple of (processed_frame, hand_landmarks)
            - processed_frame: Frame with landmarks drawn (if draw=True)
            - hand_landmarks: List of detected hand landmarks or None
        """
        # Convert BGR to RGB (MediaPipe expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        # Draw landmarks if requested
        if draw and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw_styles.get_default_hand_landmarks_style(),
                    self.mp_draw_styles.get_default_hand_connections_style()
                )
        
        return frame, results.multi_hand_landmarks
    
    def get_landmark_position(
        self,
        hand_landmarks,
        landmark_id: int,
        frame_width: int,
        frame_height: int
    ) -> Optional[Tuple[int, int]]:
        """
        Get pixel coordinates of a specific landmark.
        
        Args:
            hand_landmarks: Hand landmarks from MediaPipe
            landmark_id: ID of landmark (0-20)
            frame_width: Width of frame in pixels
            frame_height: Height of frame in pixels
            
        Returns:
            Tuple of (x, y) pixel coordinates or None if not found
        """
        if hand_landmarks is None:
            return None
        
        if 0 <= landmark_id < len(hand_landmarks.landmark):
            landmark = hand_landmarks.landmark[landmark_id]
            
            # Convert normalized coordinates (0.0-1.0) to pixels
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            
            return (x, y)
        
        return None
    
    def close(self) -> None:
        """Release MediaPipe resources."""
        if self.hands:
            self.hands.close()
            print("✅ Hand tracker closed")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close()