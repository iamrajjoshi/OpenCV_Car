import motorAPI
import time
robot = motorAPI.Drivetrain(motorAPI.Motor(1),motorAPI.Motor(4))

robot.forward(100)
time.sleep(2)
print("here")

robot.shutdown()
