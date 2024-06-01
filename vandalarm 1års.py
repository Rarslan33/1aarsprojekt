import machine
import onewire
import ds18x20
import time
import espnow
import network

station = network.WLAN(network.STA_IF)
station.active(True)

station.config(channel=1)  

esp_now = espnow.ESPNow()
esp_now.active(True)

peer = b'\xB0\xA7\x32\xDE\x1F\x0C'

esp_now.add_peer(peer)

soil_sensor_pin = machine.ADC(machine.Pin(34))  
ds_pin = machine.Pin(4)                         
      
ow = onewire.OneWire(ds_pin)
ds = ds18x20.DS18X20(ow)

roms = ds.scan()
if not roms:
    print('Ingen DS18B20 enheder fundet')
else:
    print('Fundne DS18B20 enheder: ', roms)

MOISTURE_THRESHOLD = 300
TEMPERATURE_THRESHOLD = 24.0

alarm_activated = False

while True:
    if alarm_activated:
        print('Alarm aktiveret! Vent på manuel reset...')
        esp_now.send(peer, b'Oversvømmelse!')
        time.sleep(1)
        continue

    soil_moisture_value = soil_sensor_pin.read()
    print('Jordfugtighed: {}'.format(soil_moisture_value))

    ds.convert_temp()
    time.sleep_ms(750) 
    temperature = ds.read_temp(roms[0]) if roms else None
    if temperature is not None:
        print('Temperatur: {}'.format(temperature))

        if soil_moisture_value > MOISTURE_THRESHOLD and temperature < TEMPERATURE_THRESHOLD:
            alarm_activated = True
            print('Alarm aktiveret!')
    else:
        print('Fejl: Temperatur kunne ikke læses')

    time.sleep(1) 