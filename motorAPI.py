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

    def backward(self, speed):
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.flag['f'],GPIO.LOW)
        GPIO.output(self.flag['r'],GPIO.HIGH)        

    def stop(self):
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.flag['f'],GPIO.LOW)
        GPIO.output(self.flag['r'],GPIO.LOW)

    def right(self, left, right, speed):
        left.stop()
        right.forward(speed)

    def left(self, left, right, speed):
        left.forward(speed)
        right.stop()

    def speed(self):
        self.PWM.ChangeDutyCycle(speed)

    def shutdown(self):
        GPIO.cleanup()