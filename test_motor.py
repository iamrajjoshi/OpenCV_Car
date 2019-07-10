from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
 
Motor1 = 16    # Input Pin
Motor2 = 18    # Input Pin
Motor3 = 22    # Enable Pin

Motor5 = 36
Motor4 = 32
Motor6 = 37 #Enable

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
 
GPIO.setup(Motor4,GPIO.OUT)
GPIO.setup(Motor5,GPIO.OUT)
GPIO.setup(Motor6,GPIO.OUT)


print ("BACKWARD MOTION")
GPIO.output(Motor1,GPIO.HIGH)
GPIO.output(Motor2,GPIO.LOW)
GPIO.output(Motor3,GPIO.HIGH)

GPIO.output(Motor4,GPIO.HIGH)
GPIO.output(Motor5,GPIO.LOW)
GPIO.output(Motor6,GPIO.HIGH)

sleep(3)
 
print ("FORWARD MOTION")
GPIO.output(Motor1,GPIO.LOW)
GPIO.output(Motor2,GPIO.HIGH)
GPIO.output(Motor3,GPIO.HIGH)

GPIO.output(Motor4,GPIO.LOW)
GPIO.output(Motor5,GPIO.HIGH)
GPIO.output(Motor6,GPIO.HIGH)
sleep(3)
 
print ("STOP")
GPIO.output(Motor3,GPIO.LOW)
GPIO.output(Motor6,GPIO.LOW)
 

GPIO.cleanup()