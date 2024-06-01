import machine
import utime
from machine import Pin, PWM
from time import sleep
import network
import espnow

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

station = network.WLAN(network.STA_IF)
station.active(True)
station.config(channel=1) 

esp_now = espnow.ESPNow()
esp_now.active(True)

ledblå = 26  

led_pinblå = Pin(ledblå, Pin.OUT)

ledgrøn = 25  

led_pingrøn = Pin(ledgrøn, Pin.OUT)

ledrød = 27  

led_pinrød = Pin(ledrød, Pin.OUT)

def send_data_alarm():
    while True:
        host, msg = esp_now.recv(10)
        if msg == b'Flame detected!':
            message = "Brandalarm gået\n"
            led_pinrød.on()
            uart.write(message)
            print(f"Sent: {message}")
            utime.sleep(2) 
        if msg == b'Oversvømmelse!':
            message = "oversvømmelse alarm\n"
            led_pingrøn.on()
            uart.write(message)
            print(f"Sent: {message}")
            utime.sleep(2)
        if msg == b'pirtest':
            message = "Tyverialarm gået\n"
            led_pinblå.on()
            uart.write(message)
            print(f"Sent: {message}")
            utime.sleep(2)

send_data_alarm()