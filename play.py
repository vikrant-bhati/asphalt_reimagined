import cv2
from capture_video import CaptureVideo
from hand_landmark import CaptureHandLandmarks
from controller import GameController

if __name__ == "__main__":
    video_capture = CaptureVideo()
    hand_landmarks = CaptureHandLandmarks()
    game_controller = GameController()
    try:
        while True:
            # Get the latest video framea
            frame = video_capture.get_frame()
            # Process the frame to detect hand landmarks
            processed_frame = hand_landmarks.define_landmarks(frame)
            left_hand_detected = False
            right_hand_detected = False
            current_hand_handmarks, mp_hand = hand_landmarks.get_landmarks_details()
            # Display the frame with landmarks
            if current_hand_handmarks is not None and current_hand_handmarks.multi_hand_landmarks:
                for idx, hand_handedness in enumerate(current_hand_handmarks.multi_handedness):
                    hand_label = hand_handedness.classification[0].label 
                    if hand_label == "Left":
                        left_hand_detected = True
                    elif hand_label == "Right":
                        right_hand_detected = True
                game_controller.controller(current_hand_handmarks, mp_hand, processed_frame)

            if left_hand_detected:
                cv2.rectangle(frame, (10, 10), (250, 80), (255, 255, 255), -1)  # Background box
                cv2.putText(frame, "Left Hand Plam Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2, cv2.LINE_AA)

            if right_hand_detected:
                # Display information for the right hand in the top-right corner
                frame_width = frame.shape[1]
                cv2.rectangle(frame, (frame_width - 260, 10), (frame_width - 10, 80), (255, 255, 255), -1)  # Background box
                cv2.putText(frame, "Right Hand Index Finger Detected", (frame_width - 250, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 0, 255), 2, cv2.LINE_AA)

                
            cv2.imshow("Hand Landmarks", frame)
            # Break on 'q' key press
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    finally:
        # Ensure resources are released
        video_capture.release()

