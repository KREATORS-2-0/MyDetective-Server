# import module for webcam accessing
import cv2

# Initialize the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

while True:
     # Capture frame-by-frame
     ret, frame = cap.read()

     # If frame is read correctly, ret is True
     if not ret:
          print("Can't receive frame. Exiting...")
          break
     
     # Display the resulting frame
     cv2.imshow('Webcam Feed', frame)

     # Press 'q' on the keyboard to exit
     if cv2.waitKey(1) == ord('q'):
          break
     
# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()