# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import os
from os import listdir
from os.path import isfile, join
import csv

def match_template(input_file, template_dir, template_file, visualize):
	# load the image image, convert it to grayscale, and detect edges
	template = cv2.imread(os.path.join(template_dir,template_file))
	template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	template = cv2.Canny(template, 50, 200)
	(tH, tW) = template.shape[:2]

	image = cv2.imread(input_file)
	image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	found = None

	# loop over the scales of the image
	for scale in np.arange(0.7,1.3,0.05):
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			continue

		# detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		# if we have found a new maximum correlation value, then update
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)

	# unpack the bookkeeping variable and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

	# draw a bounding box around the detected result and display the image
	if visualize:
		cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
		i = os.path.splitext(input_file)[0]
		t = os.path.splitext(template_file)[0]
		cv2.imwrite("results/"+i+"_"+t+".jpg", image)
	return maxVal, r

def wrapper(args):
	'''
	input : all cli arguments
	output : error
	'''
	# check if it's a valid directory
	template_dir = os.path.abspath(args["templates"])
	if not os.path.isdir(template_dir):
		return "Not a valid directory"
	# get list of files in that directory
	(_, _, files) = next(os.walk(template_dir))
	# remove dot files
	image_files = [f for f in files if not f.startswith(".")]
	# match template for each file found	
	with open('results.csv', mode='w') as results_file:
		writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Input image", "Template image", "Found", "Correlation", "Scale"])
		for template in image_files:
			print("Looking for %s in %s" %(template, args["inputpath"]))
			match_idx, scale = match_template(args["inputpath"], template_dir,template, args["visualize"])
			
			writer.writerow([args["inputpath"], template, match_idx>0.15, match_idx, scale])


if __name__=="__main__":
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	# ap.add_argument("-b", "--batch", action="store_true")
	ap.add_argument("-t", "--templates", required=True, help="Path to template image")
	ap.add_argument("-i", "--inputpath", required=True, help="Path to image where template will be matched")
	ap.add_argument("-v", "--visualize", action="store_true")
	args = vars(ap.parse_args())
	err = wrapper(args)
	if err:
		print("ERROR: " + err)
	elif args["visualize"]:
		print("Check results folder for the results")
	