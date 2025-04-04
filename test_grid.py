import cv2
import numpy as np
from processors.detectors.shape_detectors.grid_helper import GridHelper

# Create a blank black frame (640x480)
frame = np.zeros((480, 640, 3), dtype=np.uint8)

# Simulate 9 squares positioned in a grid (x, y, width, height)
simulated_squares = [
    (100, 100, 40, 40), (160, 100, 40, 40), (220, 100, 40, 40),  # Top row
    (100, 160, 40, 40), (160, 160, 40, 40), (220, 160, 40, 40),  # Middle row
    (100, 220, 40, 40), (160, 220, 40, 40), (220, 220, 40, 40)   # Bottom row
]

# Use the grid helper to form a grid
grid = GridHelper.form_grid(simulated_squares)

# Draw the grid on the frame
if grid:
    GridHelper.draw_grid(frame, grid)
    cv2.imshow("Test Grid", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Failed to form a valid 3x3 grid.")
