from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import motorAPI

robot = motorAPI.Drivetrain(motorAPI.Motor(4),motorAPI.Motor(1))
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
 
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
		robot.forward(50)
	if(key == ord('a')):
		robot.left(25)
	if(key == ord('s')):
		robot.reverse(50)
	if(key == ord('d')):
		robot.right(25)
	if(key == ord('b')):
		robot.stop()
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("p"):
		break
robot.shutdown()