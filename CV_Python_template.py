# This is the vision library OpenCV
import cv2
# This is a library for mathematical functions for python (used later)
import numpy as np
# This is a library to get access to time-related functionalities
import time

import cv2.aruco as aruco # Import the aruco module from OpenCV

Camera=np.load('Sample_Calibration.npz') #Load the camera calibration values
CM=Camera['CM'] #camera matrix
dist_coef=Camera['dist_coef']# distortion coefficients from the camera

marker_size = 40 # size of the ArUco marker in mm
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) 
parameters = aruco.DetectorParameters() 

# Select the first camera (0) that is connected to the machine
# in Laptops should be the build-in camera
cap = cv2.VideoCapture(0)

# Set the width and heigth of the camera to 1920x1080
cap.set(3,1920)
cap.set(4,1080)

#Create two opencv named windows
cv2.namedWindow("frame-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("gray-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("canny-image", cv2.WINDOW_AUTOSIZE)

#Position the windows next to eachother
cv2.moveWindow("frame-image",0,100)
cv2.moveWindow("gray-image",640,100)
cv2.moveWindow("canny-image",200,100)

# Execute this continuously
while(True):
    
    # Start the performance clock
    start = time.perf_counter()
    
    # Capture current frame from the camera
    ret, frame = cap.read()
    
    # Convert the image from the camera to Gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Run Aruco detection function
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Draw detected markers on the color frame if any were found.
    # Use a robust check because `ids` can be None or an empty array.
    if ids is not None and len(ids) > 0:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)

    # Apply Gaussian blur before running Canny to reduce noise
    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    # Also overlay markers on the blurred gray image so the gray window
    # shows the markers as well. Convert to BGR to draw colored markers,
    # then convert back to gray for display.
    blurred_bgr = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
    if ids is not None and len(ids) > 0:
        blurred_bgr = aruco.drawDetectedMarkers(blurred_bgr, corners, ids)
    gray_with_markers = cv2.cvtColor(blurred_bgr, cv2.COLOR_BGR2GRAY)

    # Run Canny on the blurred image
    canny = cv2.Canny(blurred, 100, 200)

    # Display the original frame in a window
    cv2.imshow('frame-image', frame)

    # Display the blurred gray image in another window
    cv2.imshow('gray-image', blurred)

    # Display the Canny edges in another window
    cv2.imshow('canny-image', canny)
    
    # Stop the performance counter
    end = time.perf_counter()
    
    # Print to console the exucution time in FPS (frames per second)
    print ('{:4.1f}'.format(1/(end - start)))

    # If the button q is pressed in one of the windows 
    if cv2.waitKey(20) & 0xFF == ord('q'):
        # Exit the While loop
        break
    

# When everything done, release the capture
cap.release()
# close all windows
cv2.destroyAllWindows()
# exit the kernel
exit(0)