import motorAPI
import getch

robot = motorAPI.Drivetrain(motorAPI.Motor(4),motorAPI.Motor(1))

while(True):
	char = getch.getch()
	if(char == 'p'):
		break
	if(char == 'w'):
		robot.forward(100)
	if(char == 'a'):
		robot.left(100)
	if(char == 's'):
		robot.reverse(100)
	if(char == 'd'):
		robot.right(100)
	if(char == 'b'):
		robot.stop()
