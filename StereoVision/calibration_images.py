import cv2

# Chessboard parameters
chessboard_size = (6, 5)  # Define the number of inner corners in the chessboard pattern

# Initialize video capture object
cap = cv2.VideoCapture(0)

# Initialize variable for image numbering
num = 0

while cap.isOpened():
    success, img = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        # Refine corner positions
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

        # Draw corners on the image
        img_with_corners = cv2.drawChessboardCorners(img, chessboard_size, corners, True)

        cv2.imshow('Camera with Corners', img_with_corners)

    # Save image when 's' key is pressed
    key = cv2.waitKey(5)
    if key == 27:  # ESC key
        break
    elif key == ord('s'):
        cv2.imwrite('images/stereo/image' + str(num) + '.png', img_with_corners)
        print("Image saved!")
        num += 1

cap.release()
cv2.destroyAllWindows()
