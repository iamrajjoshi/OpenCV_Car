
import cv2 as cv
import numpy as np
import time
from imutils.video import FPS

video_feed = cv.VideoCapture(0)
print("[INFO] starting video stream...")
time.sleep(2.0)
fps = FPS().start()

while((cv.waitKey(1) & 0xFF) != ord("q")):
    trash, frame = video_feed.read()
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    cv.imshow('Original',frame)
    frame = cv.GaussianBlur(frame, (9,9), 0)
    edges = cv.Canny(frame,100,200)
    cv.imshow('Edges',edges)
    fps.update()
    
fps.stop()
print ("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print ("[INFO] FPS: {:.2f}".format(fps.fps()))
video_feed.release()
