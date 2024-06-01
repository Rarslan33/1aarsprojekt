from machine import Pin, PWM
import network
import espnow
import time

station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)
peer = b'\xB0\xA7\x32\xDE\x1F\x0C'     
esp_now.add_peer(peer)

pir_pin = Pin(27, Pin.IN)       
trig_pin = Pin(32, Pin.OUT)     
echo_pin = Pin(33, Pin.IN)      
servo_pin = Pin(26, Pin.OUT)    
led_pin = Pin(25, Pin.OUT)      
pump_pin = Pin(12, Pin.OUT)     
buzzer_pin = Pin(14, Pin.OUT)   

servo = PWM(servo_pin, freq=50)

def set_servo_angle(angle):
    duty = int((angle / 180) * 75 + 40)
    servo.duty(duty)

def measure_distance():
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)
    pulse_duration = 0
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
        pulse_duration += time.ticks_diff(pulse_end, pulse_start)
        pulse_start = pulse_end
    distance = (pulse_duration / 2) * 0.0343
    return distance

def check_pir():
    return pir_pin.value()

def check_ultrasonic():
    return measure_distance()

def control_led(tænd):
    led_pin.value(tænd)

def control_pump(tænd):
    pump_pin.value(tænd)

def control_buzzer(tænd):
    buzzer_pin.value(tænd)

last_servo_angle = 90  
while True:
    pir_state = check_pir()
    ultrasonic_distance = check_ultrasonic()

    print("PIR sensor state:", pir_state)
    print("Ultrasonic sensor distance:", ultrasonic_distance, "cm")

    if pir_state == 1 and ultrasonic_distance < 50:
        print("ALARM! Motion detected within 50cm!")
        last_servo_angle = 90 
        set_servo_angle(last_servo_angle) 
        control_led(1)  
        control_pump(1)  
        control_buzzer(1)
        buzzer_pwm = PWM(buzzer_pin)
        esp_now.send(peer, b'pirtest')
    else:
        for angle in range(last_servo_angle, -1, -1):  
            set_servo_angle(angle)
            time.sleep_ms(10) 
        for angle in range(0, last_servo_angle + 1, 1): 
            set_servo_angle(angle)
            time.sleep_ms(10)
            
    time.sleep_ms(10) 