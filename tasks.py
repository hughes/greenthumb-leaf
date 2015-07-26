from celery import Celery
from fluent import sender, event

app = Celery('gt-leaf')
app.config_from_object('celeryconfig')
sender.setup('greenthumb')

@app.task
def photoresistor():
    import RPi.GPIO as GPIO, time
    GPIO.setmode(GPIO.BCM)

    def RCtime(RCpin):
        reading = 0
        TIMEOUT = 2000
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        while (GPIO.input(RCpin) == GPIO.LOW and reading < TIMEOUT):
            reading += 1
        return reading

    result = RCtime(18)
    print result
    event.Event('sensor', {'name': 'photodiode', 'value': result})
    return result

@app.task
def pump():
    import RPi.GPIO as GPIO, time
    GPIO.setmode(GPIO.BCM)
    
    def doPump(RCpin):
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, 1)
        event.Event('actuator', {'name': 'pump', 'state': 1})
        time.sleep(40)
        GPIO.output(RCpin, 0)
        event.Event('actuator', {'name': 'pump', 'state': 0})
    
    doPump(24)
    return 'done'
