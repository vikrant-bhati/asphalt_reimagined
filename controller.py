import math
import cv2
from pynput.keyboard import Controller
from controller_enum import Steering, Speed
import time 

class GameController:

    def __init__(self):
        self.direction = "Forward" # I will be using 4 directions i.e. Left, Right, Forward and Downwards
        self.accelerate = "Nitro"
        self.keyboard = Controller()

    def controller(self, hand_landmarks, mp_hands, frame):
        for idx, hand_landmark in enumerate(hand_landmarks.multi_hand_landmarks):
            if hand_landmarks.multi_handedness:
                hand_label = hand_landmarks.multi_handedness[idx].classification[0].label
                if hand_label == "Right":
                    index_tip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_base = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    x, y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                    prev_x, prev_y = int(index_base.x * frame.shape[1]), int(index_base.y * frame.shape[0])
                    self.steer(x,y, prev_x, prev_y)
                else:
                    index_tip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_base = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    x, y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                    prev_x, prev_y = int(index_base.x * frame.shape[1]), int(index_base.y * frame.shape[0])
                    self.accelarator(prev_y,y) 
            else:
                index_tip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_base = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                x, y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                prev_x, prev_y = int(index_base.x * frame.shape[1]), int(index_base.y * frame.shape[0])
                self.steer(x,y, prev_x, prev_y)


    def steer(self,x, y, prev_x, prev_y):
        dx = x - prev_x
        horizontal_threshold = 10
        if abs(dx) > horizontal_threshold:
            if dx > 0: 
                self.keyboard.press(Steering.RIGHT.value)
                time.sleep(0.1)
                self.keyboard.release(Steering.RIGHT.value)
            else:
                self.keyboard.press(Steering.LEFT.value)
                time.sleep(0.1)
                self.keyboard.release(Steering.LEFT.value)

    def accelarator(self, index_finger_tip, middle_finger_pip):
        if(index_finger_tip < middle_finger_pip):
            self.keyboard.press(Speed.BRAKE.value)
            time.sleep(0.1)
            self.keyboard.release(Speed.BRAKE.value)
        else:
            self.keyboard.press(Speed.ACCELERATION.value)
            time.sleep(0.1)
            self.keyboard.release(Speed.ACCELERATION.value)