import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Motor: 
    gpio_pi_pins = {1:{'e':11,'f':13,'r':15}, 4:{'e':32,'f':26,'r':24}}
    
    def __init__(self, motor):
        self.flag = self.gpio_pi_pins[motor]
        GPIO.setup(self.flag['e'],GPIO.OUT)
        GPIO.setup(self.flag['f'],GPIO.OUT)
        GPIO.setup(self.flag['r'],GPIO.OUT)
        self.PWM = GPIO.PWM(self.flag['e'], 50)
        self.PWM.start(0)
        GPIO.output(self.flag['e'],GPIO.HIGH)
        GPIO.output(self.flag['f'],GPIO.LOW)
        GPIO.output(self.flag['r'],GPIO.LOW)

    def forward(self, speed):
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.flag['f'],GPIO.HIGH)
        GPIO.output(self.flag['r'],GPIO.LOW)

    def reverse(self, speed):
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.flag['f'],GPIO.LOW)
        GPIO.output(self.flag['r'],GPIO.HIGH)        

    def stop(self):
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.flag['f'],GPIO.LOW)
        GPIO.output(self.flag['r'],GPIO.LOW)

    def shutdown(self):
        GPIO.cleanup()

class Drivetrain:
    def __init__(self, *motors):
        self.motor = []
        for i in motors:
            self.motor.append(i)

    def forward(self,speed):
        for i in range(len(self.motor)):
            self.motor[i].forward(speed)

    def reverse(self,speed):
        for i in range(len(self.motor)):
            self.motor[i].reverse(speed)

    def stop(self):
        for i in range(len(self.motor)):
            self.motor[i].stop()

    def right(self, speed): 
        self.motor[0].stop()
        self.motor[1].forward(speed)

    def left(self, speed):
        self.motor[0].forward(speed)
        self.motor[1].stop()
    
    def shutdown(self):
        for i in range(len(self.motor)):
            self.motor[i].shutdown()
        