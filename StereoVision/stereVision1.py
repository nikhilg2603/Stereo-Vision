import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import random
# Function for stereo vision and depth estimation
import triangulation as tri
import calibration

# Open both cameras
cap_right = cv2.VideoCapture(0)                    
cap_left =  cv2.VideoCapture(2)

# Stereo vision setup parameters
frame_rate = 30    # Camera frame rate (maximum at 120 fps)
B = 9               # Distance between the cameras [cm]
f = 8               # Camera lens's focal length [mm]
alpha = 56.6        # Camera field of view in the horizontal plane [degrees]

# Variable to store the click position
click_position = None

# Create a function to handle mouse events
def mouse_event(event, x, y, flags, param):
    global click_position
    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the click position
        click_position = (x,y)
                          #remove this random when actual 

# Create a named window and set the mouse callback function
cv2.namedWindow("frame right")
cv2.setMouseCallback("frame right", mouse_event)

# Main program loop for stereo vision and depth estimation
while cap_right.isOpened() and cap_left.isOpened():
    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    ################## CALIBRATION #########################################################
    frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)
    ########################################################################################

    # If cannot catch any frame, break
    if not succes_right or not succes_left:
        break

    # Convert the BGR image to RGB
    frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
    frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)

    # Show the frames
    cv2.imshow("frame right", frame_right)
    cv2.imshow("frame left", frame_left)

    # Check if a click position is available
    if click_position is not None:
        # Calculate depth at the clicked position
        depth = tri.find_depth(click_position, (click_position[0]+random.randint(1,10),click_position[1]+random.randint(1,10)), frame_right, frame_left, B, f, alpha)
        print("Depth at clicked position:", depth)
        # Reset click position to None
        click_position = None

    # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and destroy all windows before termination
cap_right.release()
cap_left.release()
cv2.destroyAllWindows()
