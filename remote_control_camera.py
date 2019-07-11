from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import motorAPI
left = motorAPI.Motor(4)
right = motorAPI.Motor(1)
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	if(key == ord('w')):
		left.forward(100)
		right.forward(100	)	
	if(key == ord('a')):
		left.forward(100)
		right.stop()
	if(key == ord('s')):
		left.stop()
		right.stop()
	if(key == ord('d')):
		right.forward(100)
		left.stop()
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("p"):
		break

left.shutdown()
right.shutdown()