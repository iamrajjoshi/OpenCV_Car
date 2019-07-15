#import motorAPI
import cv2 as cv
import numpy as np

#robot = motorAPI.Drivetrain(motorAPI.Motor(4),motorAPI.Motor(1))

frame = cv.imread('good/image2.jpg')
frame = cv.resize(frame,(820,616))
hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#cv.namedWindow("", cv.WINDOW_NORMAL)
cv.imshow('Frame', hsv)
cv.waitKey(0)
l = np.array([ 92,   4, 179] )
h = np.array([132,  44, 279])
mask = cv.inRange(hsv,l, h)
cv.imshow('Frame', mask)

cv.waitKey(0)