#"""
#Original Author: Life2coding / https://www.life2coding.com/crop-image-using-mouse-click-movement-python/
#Modified By: Marco Knabe
#Modifications:  put into class structure
#				added 3 additional 3 draw directions
#				outputs cropped image as file 
#				checks is output file already exists
#				scals shown cropped image
#"""

import cv2              # pip install opencv-python
from pathlib import Path
import os
import config

# To create our class, notice that we use the class keyword. 
# A class provides the abstract blueprint definition for an object, an instantiated version of the class.
# After the class keyword, we then define the name of the class followed by a colon. 
# Indented inside the class are functions specific to the class. 
# Notice that the first parameter for each of these functions (also called methods) is the self parameter.
class CropImage:
	
	# attributes of our class
	cropping = False								# boolean indicating whether cropping is being performed or not
	x_start, y_start, x_end, y_end = 0, 0, 0, 0		# initialize the list of reference points
	image = None
	clone = None			# copy of image
	scaleValue = 4

	# functions
	def __init__(self):
		# print('we examine this file: ', os.path.join(config.dir_media, config.file))
		# print('and than we store the cropped frame here: ', config.dir_crop)

		self.dir_work = config.dir_work
		self.dir_proj = config.dir_proj
		self.dir_media = config.dir_media
		self.dir_crop = config.dir_crop
		self.file = config.file

		# we will read an image from our file system. 
		# To do so, we call the imread function from the imported cv2 module, passing as input the path to the image. 
		self.image = cv2.imread(os.path.join(self.dir_media, self.file))

		# To know the pixels or dimensions of the image use img.shape
		print('Dimension of Image:', self.image.shape)		# just for fun

		# Note that the previous function call will return the image as a numpy ndarray. 
		# Thus, we will make use of the copy method of the ndarray class to obtain a copy of our image.
		# This method takes no arguments and returns a new ndarray that is a copy of the original one.
		self.clone = self.image.copy()

		# create window with file name as titel
		cv2.namedWindow(config.file)
		cv2.moveWindow(config.file, 400,300)  # Move it to (400,300)

		# What is 'set mouse callback' ?
		# First we create a mouse callback function which is executed when a mouse event take place. 
		# Mouse event can be anything related to mouse like left-button down, left-button up, 
		# left-button double-click etc. It gives us the coordinates (x,y) for every mouse event. 
		# With this event and location, we can do whatever we like
		#
		# after using setMouseCallback, the used function is called whenever the mouse is moved or a button is used. 
		# When calling setMouseCallback you don't CALL 'mouse_crop' but you tell setMouseCallback which function 
		# should be called on a mouse event (that's called a callback function).
		cv2.setMouseCallback(config.file, self.mouse_crop)

		# scaleFactor = 1

		# https://www.kite.com/python/answers/how-to-use-while-true-in-python
		# A while-loop executes code repeatedly as long as a given boolean condition evaluates to True. 
		# Using while True results in an infinite loop.

		# https://learnopencv.com/image-resizing-with-opencv/#resize-with-scaling-factor
		# Scaling Factor or Scale Factor is usually a number that scales or multiplies some quantity, 
		# in our case the width and height of the image. It helps keep the aspect ratio intact and preserves the display quality. 
		# So the image does not appear distorted, while you are upscaling or downscaling it.
		while True:
			i = self.image.copy()
			# if scaleFactor < 0.1:
			#	scaleFactor = 0.1
			if cv2.getWindowProperty(config.file, cv2.WND_PROP_VISIBLE) <1:		# wrong selection of ROI:
				break															# Close window by clicking on the X in the frame.
																				# Disable with Raspberry OS (compatibility problems).

			# https://www.datasciencelearner.com/cv2-waitkey-in-python-example/
			# 1.waitKey(0) will display the window infinitely until any keypress (it is suitable for image display).
			# 2.waitKey(1) will display a frame for 1 ms, after which display will be automatically closed. 
			# Since the OS has a minimum time between switching threads, the function will not wait exactly 1 ms, 
			# it will wait at least 1 ms, depending on what else is running on your computer at that time.
			# So, if you use waitKey(0) you see a still image until you actually press something 
			# while for waitKey(1) the function will show a frame for at least 1 ms only.

			# Now after reading the image let’s display the image on the window screen. 
			# To display the image you have to use the method cv2.imshow() combination with waitkey().
			
			# https://stackoverflow.com/questions/14494101/using-other-keys-for-the-waitkey-function-of-opencv

			# https://technicalmasterblog.wordpress.com/2019/07/03/whats-0xff-for-in-cv2-waitkey1/

			# Book: Raspberry Pi Computer Vision Programming: Design and implement computer vision applications:
			# In order to decide the FPS for the playback, we need to pass the appropriate argument to the call 
			# of the waitkey () function. Suppose we want to play back the video at 25 FPS, then the argument 
			# to be passed can be calculated with the 1000/25 = 40 formula. We know that waitkey () waits for 
			# the number of milliseconds. we pass to it as an argument. And, a second has 1,000 milliseconds, 
			# hence the formula. For 30 FPS, this will be 33.3.
			# If ESC key is pressed, leave 'if' loop and go on (to 'if not self.cropping:')
			
			if cv2.waitKey(40) == 27:		# wait for ESC key to exit; ASCII Table, ISO 1252 Latin-1:	27dec = ESCape
				break						# cv2.waitKey(33) 30FPS (NTSC) / cv2.waitKey(40) 25FPS (PAL)

			if not self.cropping:			# 'not' is a logical operator that evaluates to 'True' 
											# if the expression used with it is 'False'

				# cv2.imshow(window_name, image) method is used to display an image in a window. 
				# The window automatically fits to the image size. 
				#	'window_name': A string representing the name of the window in which image to be displayed. 
				#	'image': It is the image that is to be displayed.
				cv2.imshow(config.file, self.image)

			# https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
			elif self.cropping:
				# cv2.rectangle(image, start_point, end_point, color, thickness)
				cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (0, 255, 255), 1)
				cv2.imshow(config.file, i)

		cv2.destroyAllWindows()

	def mouse_crop(self, event, x, y, flags, param):
		# Anytime a mouse event happens, OpenCV will relay the pertinent details to our click_and_crop function.
		# In order for our function to handle the relay, we need to accept 5 arguments:
			# event: The event that took place (left mouse button pressed, left mouse button released, mouse movement, etc).
			# x: The x-coordinate of the event.
			# y: The y-coordinate of the event.
			# flags: Any relevant flags passed by OpenCV.
			# params: Any extra parameters supplied by OpenCV.

		# grab references to the global variables
		# Using the keyword 'global' before a variable makes this variable to the global scope
		global x_start, y_start, x_end, y_end, cropping			# grab references to the global variables

		# if the left mouse button was DOWN, start RECORDING (x, y) coordinates and 
		# indicate that cropping is being performed
		if event == cv2.EVENT_LBUTTONDOWN:
			self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
			self.cropping = True

			print('EVENT_LBUTTONDOWN: ', self.x_start, self.y_start, self.x_end, self.y_end)

		# Mouse is Moving
		elif event == cv2.EVENT_MOUSEMOVE:
			if self.cropping == True:
				self.x_end, self.y_end = x, y

		# check to see if the left mouse button was released
		elif event == cv2.EVENT_LBUTTONUP:

			# record the ending (x, y) coordinates and indicate that the cropping operation is finished
			self.x_end, self.y_end = x, y
			self.cropping = False		# cropping is finished

			print('EVENT_LBUTTONUP: ', self.x_start, self.y_start, self.x_end, self.y_end)
			
			# list of tuples [(1, 2), (3, 4), (5, 6)]
			# A tuple in Python can be created by enclosing all the comma-separated elements inside the parenthesis (). 
			# Elements of the tuple are immutable and ordered. It allows duplicate values and can have any number of elements. 
			# You can even create an empty tuple.
			refPoint = [(self.x_start, self.y_start), (self.x_end, self.y_end)]

			# We can use the index operator [] to access an item in a list. In Python, indices start at 0. 
			# The index must be an integer.
			# to access a nested data type (tuples in a list), we append the brackets to get to the innermost item. 
			# The first bracket gives you the location of the tuple in your list. 
			# The second bracket gives you the location of the item in this tuple.

			print('refPoint[0][0]: ',refPoint[0][0])
			print('refPoint[0][1]: ',refPoint[0][1])
			print('refPoint[1][0]: ',refPoint[1][0])
			print('refPoint[1][1]: ',refPoint[1][1])

			print('refPoint: ', refPoint[0][0],refPoint[0][1],refPoint[1][0],refPoint[1][1])

			# if there are two reference points, then crop the region of interest
			# from the image and display it
			# if-lines: a kind of roi-converter  -  no matter how the area is cropped, the roi starts 
			# always from top-left to bottom-left (y), than from bottom-left to bottom-right (x)

			# the following first example is probably the 'pythonic' way, but for me, as a beginner, 
			# hard to read and understand
			#if len(refPoint) == 2:		# when two points were found
			#	roi = None				# Region of Interest (ROI)
			#	if(refPoint[0][0] > refPoint[1][0]):			# mousepointer moved from right to left
			#		if(refPoint[0][1] < refPoint[1][1]):		# mp moved from top to bottom
			#			roi = self.clone[refPoint[0][1]:refPoint[1][1], refPoint[1][0]:refPoint[0][0]]
			#		if(refPoint[0][1] > refPoint[1][1]):		# mp moved from bottom to top
			#			roi = self.clone[refPoint[1][1]:refPoint[0][1], refPoint[1][0]:refPoint[0][0]]
			#	if(refPoint[0][0] < refPoint[1][0]):			# mp moved from left to right
			#		if(refPoint[0][1] < refPoint[1][1]):		# mp moved from top to bottom
			#			roi = self.clone[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
			#		if(refPoint[0][1] > refPoint[1][1]):		# mp moved from bottom to top
			#			roi = self.clone[refPoint[1][1]:refPoint[0][1], refPoint[0][0]:refPoint[1][0]]

			# second example
			# https://stackoverflow.com/questions/48941504/problems-while-cropping-roi-with-mouse-using-open-cv
			# draw my ROI on a paper, choose ? select the x and y values, and i can see and learn, 
			# that it does not matter how the area is cropped, the result (ROI) is always from top 
			# to bottom, and from left to right

			# if there are two reference points, then crop the region of interest
			# from the image and display it
			if len(refPoint) == 2:		# when two points were found
				roi = None				# Region of Interest (ROI)
				x_start = refPoint[0][0]
				y_start = refPoint[0][1]
				x_end = refPoint[1][0]
				y_end = refPoint[1][1]
				x_big, x_small = ((x_start, x_end) if x_start>x_end else (x_end, x_start))
				y_big, y_small = ((y_start, y_end) if y_start>y_end else (y_end, y_start))

				print('    x_start: ', x_start)
				print('    x_end: ', x_end)
				print('    y_start: ', y_start)
				print('    y_end: ', y_end)
				print('        y_small: ', y_small)
				print('        y_big: ', y_big)
				print('        x_small: ', x_small)
				print('        x_big: ', x_big)

				roi = self.clone[y_small:y_big, x_small:x_big]    

				outputFile = Path(config.file + config.outputFileExtension)
				print('outputFile (with two extensions): ', outputFile)

				# https://www.pythonpool.com/python-get-filename-without-extension/
				config.file_base = (os.path.basename(config.file).split('.')[0])
				print('filename without extension: ',config.file_base)
				
				# Syntax: cv2.imwrite(filename, image)
				# Parameters: 
				#	filename: A string representing the file name. The filename must include image format like .jpg, .png, etc
				#	image: It is the image that is to be saved. (numpy ndarray)
				#	Return Value: It returns true if image is saved successfully.
				config.imwrite_Path = os.path.join(config.dir_crop, config.file_base + "." + config.outputFileExtension)
				print('imwrite_Path: ', config.imwrite_Path)
				cv2.imwrite(config.imwrite_Path, roi)
				
				scaleX = self.scaleValue
				scaleY = self.scaleValue

				# https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
				scaleUp = cv2.resize(roi, None, fx= scaleX, fy= scaleY)

				# cv2.imshow(window_name, image) method is used to display an image in a window. 
				# The window automatically fits to the image size. 
				#	'window_name': A string representing the name of the window in which image to be displayed. 
				#	'image': It is the image that is to be displayed.
				cv2.imshow(config.file_base, scaleUp)
