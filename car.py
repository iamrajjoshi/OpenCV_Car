import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math
import sys

def roi(image, vertices):
    mask = np.zeros_like(image)
    match_mask_color = 255
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image

def draw_lines(image, lines, color=[255, 0, 0], thickness=3):
    if type(lines) == type(None):
            return image
    image = np.copy(image)
    line_img = np.zeros(( image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv.line(line_img, (x1, y1), (x2, y2), color, thickness)
    image = cv.addWeighted(image, 0.8, line_img, 1.0, 0.0)
    return image

def process(image):
    roi_vertices = [
    (0, 480),
    (0, 250),
    (640, 250),
    (640,480),
    ]

    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    canny_image = cv.Canny(gray_image, 100, 200)
    cropped_image = roi( canny_image, np.array([roi_vertices], np.int32))
    lines = cv.HoughLinesP(
        cropped_image,
        rho=10,
        theta=np.pi / 360,
        threshold=20,
        lines=np.array([]),
        minLineLength=25,
        maxLineGap= 75
    )
    count = 0
    slope = 0
    if type(lines) != type(None):
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = slope + (((y2-y1)/(x2-x1)))
                count = count + 1
        slope = slope / count
        
    line_image = draw_lines(image, lines)
    
    #configuration
    if slope < 0:
        direction = "Turn Right"
    elif slope > 0:
        direction = "Turn Left"
    else:
        direction = "Keep Straight"
    
    cv.putText(line_image, direction, (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
    cv.putText(line_image, str(slope), (50,100), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
    cv.imshow('Frame', line_image)
    return

#video to live feed
cap = cv.VideoCapture(sys.argv[1])

if ((cap.isOpened() == False)):
    print("Error: Video not found")

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        process(frame)
        if ((cv.waitKey(25) & 0xFF) == ord("q")):
            break
    else:
        break
        
cap.release()
cv.destroyAllWindows()