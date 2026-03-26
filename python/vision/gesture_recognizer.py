"""
Gesture Recognition Module

Rule-based gesture detection using hand landmark positions.
"""

from typing import Optional, Dict, List, Tuple
import math


class GestureRecognizer:
    """
    Recognizes hand gestures using rule-based analysis of landmarks.
    
    Supports gestures:
    - FIST: All fingers closed
    - OPEN_PALM: All fingers extended
    - POINTING: Only index finger extended
    - PEACE: Index and middle fingers extended
    - THUMBS_UP: Only thumb extended
    """
    
    # Landmark IDs for each finger
    THUMB_TIP = 4
    THUMB_IP = 3
    THUMB_MCP = 2
    
    INDEX_TIP = 8
    INDEX_DIP = 7
    INDEX_PIP = 6
    INDEX_MCP = 5
    
    MIDDLE_TIP = 12
    MIDDLE_DIP = 11
    MIDDLE_PIP = 10
    MIDDLE_MCP = 9
    
    RING_TIP = 16
    RING_DIP = 15
    RING_PIP = 14
    RING_MCP = 13
    
    PINKY_TIP = 20
    PINKY_DIP = 19
    PINKY_PIP = 18
    PINKY_MCP = 17
    
    WRIST = 0
    
    def __init__(self):
        """Initialize gesture recognizer."""
        self.gesture_history = []  # Store last N gestures
        self.history_size = 5      # Smooth over 5 frames
    
    def _is_finger_extended(
        self,
        hand_landmarks,
        tip_id: int,
        pip_id: int,
        mcp_id: int
    ) -> bool:
        """
        Determine if a finger is extended.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            tip_id: Fingertip landmark ID
            pip_id: PIP joint landmark ID
            mcp_id: MCP joint (knuckle) landmark ID
            
        Returns:
            True if finger is extended (straightened)
        """
        # Get landmark positions
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[pip_id]
        mcp = hand_landmarks.landmark[mcp_id]
        
        # For fingers (not thumb): extended if tip is above MCP
        # Y-axis: 0 at top, 1 at bottom (so lower Y = higher position)
        return tip.y < pip.y
    
    def _is_thumb_extended(self, hand_landmarks) -> bool:
        """
        Determine if thumb is extended.
        
        Thumb logic is different - check horizontal distance from wrist.
        """
        thumb_tip = hand_landmarks.landmark[self.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[self.THUMB_IP]
        wrist = hand_landmarks.landmark[self.WRIST]
        
        # Calculate distance from thumb tip to wrist
        tip_dist = abs(thumb_tip.x - wrist.x)
        ip_dist = abs(thumb_ip.x - wrist.x)
        
        # Extended if tip is farther from wrist than IP joint
        return tip_dist > ip_dist
    
    def get_finger_states(self, hand_landmarks) -> Optional[Dict[str, bool]]:
        """
        Get the state (extended/folded) of all fingers.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            Dictionary with finger names and their states
        """
        if not hand_landmarks:
            return None
        
        # Get first hand (we're only tracking one)
        hand = hand_landmarks[0]
        
        return {
            'thumb': self._is_thumb_extended(hand),
            'index': self._is_finger_extended(hand, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP),
            'middle': self._is_finger_extended(hand, self.MIDDLE_TIP, self.MIDDLE_PIP, self.MIDDLE_MCP),
            'ring': self._is_finger_extended(hand, self.RING_TIP, self.RING_PIP, self.RING_MCP),
            'pinky': self._is_finger_extended(hand, self.PINKY_TIP, self.PINKY_PIP, self.PINKY_MCP)
        }
    
    def recognize_gesture(self, hand_landmarks) -> Optional[str]:
        """
        Recognize gesture based on finger states.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            Gesture name or None if no hand detected
        """
        if not hand_landmarks:
            return None
        
        # Get finger states
        fingers = self.get_finger_states(hand_landmarks)
        if not fingers:
            return None
        
        # Count extended fingers
        extended_count = sum(fingers.values())
        
        # Gesture recognition rules
        gesture = "UNKNOWN"
        
        # All fingers closed
        if extended_count == 0:
            gesture = "FIST"
        
        # All fingers extended
        elif extended_count == 5:
            gesture = "OPEN_PALM"
        
        # Only index finger
        elif fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            gesture = "POINTING"
        
        # Index and middle (peace sign)
        elif fingers['index'] and fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            gesture = "PEACE"
            
        # Index and middle (peace sign)
        elif not fingers['index'] and fingers['middle'] and not fingers['ring'] and not fingers['pinky'] and fingers['thumb']:
            gesture = "RIGHT BACK AT YOU"
        
        # Only thumb
        elif fingers['thumb'] and not fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            gesture = "THUMBS_UP"
        
        # Add to history for smoothing
        self.gesture_history.append(gesture)
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Return most common gesture in history
        if self.gesture_history:
            return max(set(self.gesture_history), key=self.gesture_history.count)
        
        return gesture
    
    def get_finger_count(self, hand_landmarks) -> int:
        """
        Count how many fingers are extended.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            Number of extended fingers (0-5)
        """
        fingers = self.get_finger_states(hand_landmarks)
        if not fingers:
            return 0
        return sum(fingers.values())