
import cv2
import numpy

from CropImage import CropImage

from pathlib import Path

cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

image = cv2.imread('image/0.png')
oriImage = image.copy()

cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)

while True:

	i = image.copy()

	if not cropping:
		cv2.imshow("image", image)

	elif cropping:
		cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
		cv2.imshow("image", i)

	cv2.waitKey(1)

# close all open windows
cv2.destroyAllWindows()