import cv2
import os
import platform
import config

from crop_image import CropImage as CI

def main():

	# there are many types of mouse events. these events can be displayed by running the following line
	[print(i) for i in dir(cv2) if 'EVENT' in i]

	# https://stackoverflow.com/questions/60014652/create-relative-path-and-being-os-independent

	path = os.path.basename(__file__)
	run_on=platform.system()
	print('our os platform is: ',run_on)

	if run_on=='Windows': path=f'.\\{path}'
	elif run_on=='Linux': path=f'./{path}'

	print(f'path is {path}')
	
	# https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
	# the absolute path to the file we’re in at runtime:
	print('absolute path: ', __file__)

	# Getting the folder path of the file we’re executing
	config.dir_work = (os.path.dirname(__file__))
	
	print('folder path: ', config.dir_work)
	
	config.dir_proj = (os.path.join(config.dir_work, 'project'))
	print('project directory: ', config.dir_proj)
	
	config.dir_media = (os.path.join(config.dir_proj, 'media'))
	print('media directory: ', config.dir_media)
	
	config.dir_crop = (os.path.join(config.dir_proj, 'cropped'))
	print('cropped directory: ', config.dir_crop)

	# return a list containing the names of the entries in the directory given by 'path' ,
	# here our 'media directory'
	list_of_image_files = os.listdir(config.dir_media)
	print("\n", "list of all files in our 'media directory' :", '\n')
	for file in list_of_image_files:
		print("   ", file)
		config.file = file
		CI()

# close all open windows
cv2.destroyAllWindows()

if __name__ == "__main__":
	main()