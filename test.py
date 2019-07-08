import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from moviepy.editor import VideoFileClip
from IPython.display import HTML
import sys

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    if lines.size() == 0:
            return
    img = np.copy(img)
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8,
    )
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    return img

def pipeline(image):
    region_of_interest_vertices = [
    (0, 480),
    (0, 250),
    (640, 250),
    (640,480),
    ]

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cannyed_image = cv2.Canny(gray_image, 100, 200)
    cropped_image = region_of_interest(
        cannyed_image,
        np.array([region_of_interest_vertices], np.int32)
    )

    lines = cv2.HoughLinesP(
        cropped_image,
        rho=10,
        theta=np.pi / 360,
        threshold=50,
        lines=np.array([]),
        minLineLength=50,
        maxLineGap= 100
    )


    lc = 0
    rc = 0
    left = np.array([[0,0,0,0]],np.int64)
    right = np.array([[0,0,0,0]],np.int64)
    #print(lines)
    ''' 
    for line in lines:
        for x1, y1, x2, y2 in line:
            print(((y2-y1)/(x2-x1)))
            if ((y2-y1)/(x2-x1)) > 0:
                rc = rc+1
                temp = np.array([[x1,y1,x2,y2]],np.int64)
                right = np.add(temp, right)
            else:
                lc = lc+1
                temp = np.array([[x1,y1,x2,y2]],np.int64)
                left = np.add(temp, left)

    right = np.divide(right,rc)
    left = np.divide(left,lc)
    lines = np.array([left,right],np.int64)
    print(lines)
    '''
    line_image = draw_lines(image, lines)
    #plt.figure()
    #plt.imshow(line_image)
    #plt.figure()
    #plt.imshow(cannyed_image)
    #plt.show()
    return line_image

#image = mpimg.imread(sys.argv[1])
#pipeline(image)

white_output = sys.argv[2]
clip1 = VideoFileClip(sys.argv[1])
white_clip = clip1.fl_image(pipeline)
print("here")
white_clip.write_videofile(white_output, audio=False)
