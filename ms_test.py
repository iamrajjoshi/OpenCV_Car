import PiMotor
import time



left = PiMotor.Motor("MOTOR4",2)
right = PiMotor.Motor("MOTOR1",2)

left.forward(100)
right.forward(100)

time.sleep(3)

left.reverse(100)

time.sleep(3)

left.stop()
right.stop()
