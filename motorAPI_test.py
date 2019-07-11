import motorAPI
import time

left = PiMotor.Motor(4,2)
right = PiMotor.Motor(1,2)

left.forward(100)
right.forward(100)

time.sleep(3)

left.stop()
right.stop()

GPIO.cleanup()
