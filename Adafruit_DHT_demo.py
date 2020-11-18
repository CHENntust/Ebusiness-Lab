import dht11,time
import RPi.GPIO as GPIO

def data_filter(result):
    while result.humidity==0 and result.temperature==0:
        #obtain noise data, read snesor data again.
        result = instance.read()
    return result.humidity,result.temperature

GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=4)
while True:
    result = instance.read()
    h, t = data_filter(instance.read())
    print('濕度為',h,',溫度為',t,'℃')
    time.sleep(1)
