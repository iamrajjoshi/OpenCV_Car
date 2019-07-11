import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Motor:
    motorpins = {1:{'e':11,'f':13,'r':15}, 4:{'e':32,'f':26,'r':24}}
    
    def __init__(self, motor):
        self.pin = self.motorpins[motor]
        GPIO.setup(self.pin['e'],GPIO.OUT)
        GPIO.setup(self.pin['f'],GPIO.OUT)
        GPIO.setup(self.pin['r'],GPIO.OUT)
        self.PWM = GPIO.PWM(self.pin['e'], 50)
        self.PWM.start(0)
        GPIO.output(self.pin['e'],GPIO.HIGH)
        GPIO.output(self.pin['f'],GPIO.LOW)
        GPIO.output(self.pin['r'],GPIO.LOW)

    def forward(self, speed):
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.pin['f'],GPIO.HIGH)
        GPIO.output(self.pin['r'],GPIO.LOW)

    def stop(self):
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.pin['f'],GPIO.LOW)
        GPIO.output(self.pin['r'],GPIO.LOW)

    def speed(self):
        self.PWM.ChangeDutyCycle(speed)

    def shutdown(self):
        GPIO.cleanup()