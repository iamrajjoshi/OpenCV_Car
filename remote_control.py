import motorAPI
import getch

left = motorAPI.Motor(4)
right = motorAPI.Motor(1)

while(True):
	char = getch.getch()
	if(char == 'p'):
		break
	if(char == 'w'):
		left.forward(100)
		right.forward(100)
	if(char == 'a'):
		left.forward(50)
		right.stop()
	if(char == 's'):
		left.stop()
		right.stop()
	if(char == 'd'):
		right.forward(50)
		left.stop()

left.shutdown()
right.shutdown()