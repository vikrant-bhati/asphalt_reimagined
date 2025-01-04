import cv2

"""
This class will be used for opening the camera and using it for video stream
"""
class CaptureVideo:

    def __init__(self):
        # Initialize the webcam
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    def get_frame(self):
        resp, frame = self.capture.read()
        if not resp:
            raise Exception("Failed to capture video frame")
        # Flip the frame (mirror effect)
        frame = cv2.flip(frame, 1)
        # return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   
        return frame
    
    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()
