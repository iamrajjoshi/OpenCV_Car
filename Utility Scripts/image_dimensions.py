import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import sys

image = mpimg.imread(sys.argv[1])
image = cv2.resize(image,(320,240))
plt.imshow(image)
plt.show()