import cv2
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break

