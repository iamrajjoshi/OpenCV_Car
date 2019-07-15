#import motorAPI
import cv2 as cv
import numpy as numpy

#robot = motorAPI.Drivetrain(motorAPI.Motor(4),motorAPI.Motor(1))

frame = cv.imread('good/image2.jpg')
hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
cv.imshow('Frame', hsv)

cv.waitKey(0)