import mediapipe as mp

"""
This class is for hand landmark detection
For this we are using the google's hand landarmark detection using python library
https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python
"""

class CaptureHandLandmarks:

    def __init__(self, maxHands=2, min_detection_confidence = 0.6, min_tracking_confidence= 0.6):
        self.mp_hands = mp.solutions.hands #This is the define which model we will be using from mediapipe
        self.hands = self.mp_hands.Hands(max_num_hands = maxHands, #what are the maximum number of hands that we will be detecting
                            min_detection_confidence = min_detection_confidence, #confidence for hand detection
                            min_tracking_confidence = min_tracking_confidence) #confidence for finger detection
        self.draw_hand = mp.solutions.drawing_utils #This is to draw the hand
        self.hand_landmarks = None


    def define_landmarks(self, color_frame):    
        self.hand_landmarks = self.hands.process(color_frame)
        if self.hand_landmarks.multi_hand_landmarks:
            for hand_landmarks in self.hand_landmarks.multi_hand_landmarks:
                self.draw_hand.draw_landmarks(color_frame, hand_landmarks,self.mp_hands.HAND_CONNECTIONS)
        return color_frame
    
    def get_landmarks_details(self):
        return self.hand_landmarks, self.mp_hands


