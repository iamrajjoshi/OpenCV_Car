import motorAPI
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
robot = motorAPI.Drivetrain(motorAPI.Motor(4),motorAPI.Motor(1))

fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter('3.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
	ret, frame = cap.read()
	if ret==True:
		out.write(frame)
		cv2.imshow("Frame", frame)
	else:
		break
	
	key = cv2.waitKey(1) & 0xFF
	if(key == ord('w')):
		robot.forward(20)
	if(key == ord('a')):
		robot.left(25)
	if(key == ord('s')):
		robot.reverse(50)
	if(key == ord('d')):
		robot.right(25)
	if(key == ord('b')):
		robot.stop()
	if(key == ord('p')):
		break

cap.release()
out.release()
cv2.destroyAllWindows()