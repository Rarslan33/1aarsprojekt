import machine
import time
import network
import espnow
from time import sleep
from machine import Pin
from machine import ADC, Pin

adc = ADC(Pin(34))  
adc.width(ADC.WIDTH_10BIT) 
adc.atten(ADC.ATTN_11DB)

flame_sensor_pin = Pin(26, Pin.IN)

station = network.WLAN(network.STA_IF)
station.active(True)

station.config(channel=1) 

esp_now = espnow.ESPNow()
esp_now.active(True)

peer = b'\xB0\xA7\x32\xDE\x1F\x0C'

esp_now.add_peer(peer)

def check_flame():
    if flame_sensor_pin.value() == 1:
        print("Flame detected!")
              
while True:
    sensor_value = adc.read() 
    print("Flame Sensor Value:", sensor_value)      
    if flame_sensor_pin.value() == 1:
        print("sent")
        esp_now.send(peer, b'Flame detected!')
    time.sleep(1)