# This is the vision library OpenCV
import cv2
# This is a library for mathematical functions for python (used later)
import numpy as np
# This is a library to get access to time-related functionalities
import time

def probe_resolutions(cap, candidates=None, wait=0.1):
    """Try setting each candidate resolution and read back what the camera accepted."""
    if candidates is None:
        candidates = [
            (1920,1080),(1600,1200),(1280,1024),(1280,960),
            (1280,720),(1024,768),(800,600),(640,480),
            (640,360),(320,240)
        ]
    supported = []
    for w,h in candidates:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        time.sleep(wait)  # give camera/driver a moment
        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if actual_w == w and actual_h == h:
            supported.append((w,h))
        else:
            # some cameras report scaled/nearest size; treat equals as support
            # you can include near matches if desired
            pass
    return supported

# Select the first camera (0) that is connected to the machine
# in Laptops should be the build-in camera
cap = cv2.VideoCapture(0)

# Verify the camera opened; try a few alternate indices if not
if not cap.isOpened():
    print("Warning: camera index 0 not opened. Trying other indices...")
    for i in range(1,4):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Opened camera index {i}")
            break
    else:
        raise SystemExit("Error: could not open any camera (indices 0-3).")

# Probe before forcing other settings
print("Probing common resolutions...")
supported = probe_resolutions(cap)
print("Supported resolutions (exact matches):", supported)

# Try to use 1920x1080 if available, otherwise pick the highest supported
preferred = (1920, 1080)
if preferred in supported:
    use_w, use_h = preferred
elif supported:
    # pick the first supported in the probed list (which is ordered high->low)
    use_w, use_h = supported[0]
    print(f"Preferred {preferred} not supported; falling back to {use_w}x{use_h}")
else:
    # fallback to a common safe size
    use_w, use_h = (640, 480)
    print(f"No exact-match supported resolutions found; falling back to {use_w}x{use_h}")

# Apply chosen resolution and verify
cap.set(cv2.CAP_PROP_FRAME_WIDTH, use_w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, use_h)
time.sleep(0.1)
actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Camera using resolution: {actual_w}x{actual_h}")

#Create two opencv named windows
cv2.namedWindow("frame-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("gray-image", cv2.WINDOW_AUTOSIZE)

#Position the windows next to eachother
cv2.moveWindow("frame-image",0,100)
cv2.moveWindow("gray-image",640,100)

# Execute this continuously
while(True):
    
    # Start the performance clock
    start = time.perf_counter()
    
    # Capture current frame from the camera
    ret, frame = cap.read()

    # Handle failed/empty capture gracefully (prevent cvtColor assertion)
    if not ret or frame is None or getattr(frame, 'size', 0) == 0:
        print("Warning: empty frame captured (ret={}, frame={}). Retrying...".format(ret, None if frame is None else 'ok'))
        time.sleep(0.05)
        continue

    # Convert the image from the camera to Gray scale
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        print("cvtColor failed for this frame:", e)
        continue
    
    # Display the original frame in a window
    cv2.imshow('frame-image',frame)

    # Display the grey image in another window
    cv2.imshow('gray-image',gray)
    
    # Stop the performance counter
    end = time.perf_counter()
    
    # Print to console the exucution time in FPS (frames per second)
    #print ('{:4.1f}'.format(1/(end - start)))

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