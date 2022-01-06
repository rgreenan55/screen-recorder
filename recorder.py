# Imports
import os
import ctypes
import cv2 as cv
import numpy as np
from util import getResolution
from mss import mss

with mss() as sct:
  # Gets Screen Resolution
  user32 = ctypes.windll.user32
  user32.SetProcessDPIAware()
  [width, height] = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
  
  # Define Video Type
  codec = cv.VideoWriter_fourcc(*"mp4v")
  out = cv.VideoWriter("video.mp4", codec, 7, (width, height))

  # Live Video Display
  cv.namedWindow("Live", cv.WINDOW_NORMAL)
  cv.resizeWindow("Live", 480, 270)

  # Gets Desired Monitor
  monitor_number = 1
  monitor_data = sct.monitors[monitor_number]

  # Monitor Data
  monitor = {
    "top": monitor_data["top"],
    "left": monitor_data["left"],
    "width": width,
    "height": height,
  }

  while True:
    # Grabs Frame + Converts to Numpy Array + Converts Color
    frame = np.array(sct.grab(monitor))

    out.write(frame)
    cv.imshow("Live", frame)

    # Exits if Q is pressed
    if cv.waitKey(1) == ord('q'):
      break

# Cleanup
out.release()
cv.destroyAllWindows()

os.rename("video.mp4", "recording.mp4")