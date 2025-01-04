import time
from pynput.keyboard import Controller
from controller_enum import Steering, Speed
import matplotlib.pyplot as plt

class GameController2:

    def __init__(self):
        self.direction = "Forward"  # Possible directions: Left, Right, Forward, Downwards
        self.accelerate = "Nitro"
        self.keyboard = Controller()
        self.ground_truth = []  # To store true gestures for accuracy calculation
        self.predictions = []  # To store system-predicted gestures
        self.latency_records = []  # To store latency measurements

    def controller(self, hand_landmarks, mp_hands, frame):
        start_time = time.time()  # Record gesture start time for latency

        for idx, hand_landmark in enumerate(hand_landmarks.multi_hand_landmarks):
            if hand_landmarks.multi_handedness:
                hand_label = hand_landmarks.multi_handedness[idx].classification[0].label
                if hand_label == "Right":
                    index_tip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_base = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    x, y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                    prev_x, prev_y = int(index_base.x * frame.shape[1]), int(index_base.y * frame.shape[0])
                    self.predictions.append("Right")  # Predicted gesture
                    self.steer(x, y, prev_x, prev_y)
                else:
                    index_tip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_base = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    x, y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                    prev_x, prev_y = int(index_base.x * frame.shape[1]), int(index_base.y * frame.shape[0])
                    self.predictions.append("Left")  # Predicted gesture
                    self.accelarator(prev_y, y)

        # Measure latency
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        self.latency_records.append(latency)

    def steer(self, x, y, prev_x, prev_y):
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
        if index_finger_tip < middle_finger_pip:
            self.keyboard.press(Speed.BRAKE.value)
            time.sleep(0.1)
            self.keyboard.release(Speed.BRAKE.value)
        else:
            self.keyboard.press(Speed.ACCELERATION.value)
            time.sleep(0.1)
            self.keyboard.release(Speed.ACCELERATION.value)

    def calculate_metrics_and_plot(self):
        # Gesture Detection Accuracy
        correct_predictions = sum([1 for gt, pred in zip(self.ground_truth, self.predictions) if gt == pred])
        accuracy = (correct_predictions / len(self.ground_truth)) * 100 if self.ground_truth else 0

        # Average Latency
        avg_latency = sum(self.latency_records) / len(self.latency_records) if self.latency_records else 0

        print(f"Gesture Detection Accuracy: {accuracy:.2f}%")
        print(f"Average Latency: {avg_latency:.2f} ms")

        # Plot Latency Graph
        plt.figure(figsize=(10, 6))
        plt.plot(self.latency_records, marker='o', linestyle='-', color='blue', label="Latency (ms)")
        plt.title("Latency Over Time")
        plt.xlabel("Gesture Count")
        plt.ylabel("Latency (ms)")
        plt.grid(True)
        plt.legend()
        plt.show()
