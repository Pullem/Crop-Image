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
import numpy as np
from pathlib import Path
import os
import config

# To create our class, notice that we use the class keyword. 
# A class provides the abstract blueprint definition for an object, an instantiated version of the class.
# After the class keyword, we then define the name of the class followed by a colon. 
# Indented inside the class are functions specific to the class. 
# Notice that the first parameter for each of these functions (also called methods) is the self parameter.
class CropImage:
	
	# imagePath = None
	# imageName = None
	# cropPath = None
	
	# attributes of our class
	cropping = False								# boolean indicating whether cropping is being performed or not
	x_start, y_start, x_end, y_end = 0, 0, 0, 0		# initialize the list of reference points
	image = None
	clone = None
	outputFileName = 'cr'

	# outputFileName = os.path.join(cropPath, imageName)
	# outputFileName = dir_write
	# outputFileExtension = '.png'
	scaleValue = 4

	# functions
	# def __init__(self, dir_media, file, dir_crop):
	def __init__(self):
		print('we examine this file: ', os.path.join(config.dir_media, config.file))
		print('and than we store the cropped frame here: ', config.dir_crop)

		self.cropPath = config.dir_crop

		# we will read an image from our file system. 
		# To do so, we will call the imread function from the imported cv2 module, passing as input the path to the image. 
		# self.image = cv2.imread(imageName)
		self.image = cv2.imread(os.path.join(config.dir_media, config.file))

		# To know the pixels or dimensions of the image use img.shape
		print('Dimension of Image:', self.image.shape)

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

		scaleFactor = 1

		# https://www.kite.com/python/answers/how-to-use-while-true-in-python
		# A while-loop executes code repeatedly as long as a given boolean condition evaluates to True. 
		# Using while True results in an infinite loop.
		while True:
			i = self.image.copy()
			if scaleFactor < 0.1:
				scaleFactor = 0.1
			if cv2.getWindowProperty(config.file, cv2.WND_PROP_VISIBLE) <1:		# Close window by clicking on the X in the frame.
				break															# Disable with Raspberry OS (compatibility problems).

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

			# Book: Raspberry Pi Computer Vision Programming: Design and implement computer vision applications
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

			elif self.cropping:
				cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (0, 255, 255), 1)
				cv2.imshow(config.file, i)
			
			cv2.waitKey(1)
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
		# self.file_CI = file_CI

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

			# record the ending (x, y) coordinates and indicate that
			# the cropping operation is finished
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

			# https://stackoverflow.com/questions/48941504/problems-while-cropping-roi-with-mouse-using-open-cv
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
				roi = self.clone[y_small:y_big, x_small:x_big]    

				# outputFile = Path(self.outputFileName + self.outputFileExtension)
				outputFile = Path(config.file + config.outputFileExtension)
				print('outputFile (with two extensions): ', outputFile)

				# https://www.pythonpool.com/python-get-filename-without-extension/
				config.file_base = (os.path.basename(config.file).split('.')[0])
				# config.file_base = file_base
				print('filename without extension: ',config.file_base)

				#fileNameCounter = 0
				#while outputFile.is_file():
				#	fileNameCounter+=1
				#	outputFile = Path(self.outputFileName + str(fileNameCounter) + self.outputFileExtension)    
				#if(fileNameCounter > 0):
				#	# print('Output File Name: ' + self.outputFileName + str(fileNameCounter) + self.outputFileExtension)
				#	# cv2.imwrite(self.outputFileName + str(fileNameCounter) + self.outputFileExtension, roi)
				#	print('Output File Name: ' +self.cropPath +'\\' +self.outputFileName + str(fileNameCounter) + self.outputFileExtension)
				
				# Syntax: cv2.imwrite(filename, image)
				# Parameters: 
				#	filename: A string representing the file name. The filename must include image format like .jpg, .png, etc
				#	image: It is the image that is to be saved. (numpy ndarray)
				#	Return Value: It returns true if image is saved successfully.
				# cv2.imwrite(self.cropPath +'\\' + self.outputFileName + str(fileNameCounter) + self.outputFileExtension, roi)
				# imwrite_path = os.path.join(config.dir_crop, config.file, config.outputFileExtension)
				config.imwrite_Path = os.path.join(config.dir_crop, config.file_base + "." + config.outputFileExtension)
				# config.imwrite_path = imwrite_Path
				print('imwrite_Path: ', config.imwrite_Path)
				# cv2.imwrite(self.cropPath +'\\' + self.outputFileName + str(fileNameCounter) + self.outputFileExtension, roi)
				cv2.imwrite(config.imwrite_Path, roi)

				#else:
				#	print('Output File Name: ' + self.outputFileName + self.outputFileExtension)
				#	cv2.imwrite(self.outputFileName + self.outputFileExtension, roi)
				
				scaleX = self.scaleValue
				scaleY = self.scaleValue
				scaleUp = cv2.resize(roi, None, fx= scaleX, fy= scaleY)

				# cv2.imshow(window_name, image) method is used to display an image in a window. 
				# The window automatically fits to the image size. 
				#	'window_name': A string representing the name of the window in which image to be displayed. 
				#	'image': It is the image that is to be displayed.
				cv2.imshow(config.file_base, scaleUp)

				## if the 'r' key is pressed, reset the cropping region
				#if cv2.waitKey(40) == ord("r"):
				#	self.clone = self.image.copy()