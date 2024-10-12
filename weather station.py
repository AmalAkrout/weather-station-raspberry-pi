from machine import Pin
from machine import Pin,ADC
import dht
import machine
import time
import urequests 
import network
from vent import vitesse



HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '**************'  
 
ssid ='***********'
password ='**************'

led_net = machine.Pin(12, machine.Pin.OUT)
led_rp = machine.Pin(14, machine.Pin.OUT)

try:
   led_rp.value(0)
   led_net.value(0)
   print('démarrage de systéme')
   time.sleep(2)
   led_rp.value(1)
except KeyboardInterrupt:
    pass  

# Configure Pico W as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
 
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected(): pass
print('network config:', sta_if.ifconfig()[0])
led_net.value(1)


# Configuration du GPIO 4 pour le DHT11
dht11 = dht.DHT11(machine.Pin(4))

# Configuration du GPIO 16 pour le capteur de pluie
rain_sensor = machine.Pin(16, machine.Pin.IN)

# Configuration du GPIO pour le photoresistor
ldr_pin = Pin(26)
ldr_adc = ADC(ldr_pin)

# Seuil de luminosité pour distinguer le jour de la nuit
threshold = 500
while True:
    try:
        dht11.measure()
        temp = dht11.temperature()
        humidity = dht11.humidity()
        print('Temperature: {}C'.format(temp))
        print('Humidity: {}%'.format(humidity))
    except OSError as e:
        print('Failed to read sensor.')
        
 # Lire la valeur de luminosité du capteur LDR
    ldr_value = ldr_adc.read_u16()

    # Déterminer si c'est le jour ou la nuit
    if ldr_value > threshold:
        print("Il fait jour. Luminosité =", ldr_value)
    else:
        print("Il fait nuit. Luminosité =", ldr_value)

        
    x=0
    # Lire la valeur du capteur de pluie
    rain_value = rain_sensor.value()
    # Afficher la valeur du capteur de pluie
    if rain_value == 0:
        print("Pas de pluie. Valeur du capteur de pluie =", rain_value)
        x=0
    else:
        print("Il pleut ! Valeur du capteur de pluie =", rain_value)
        x=1

    windspeed=vitesse()
     
    # Envoyer les données à ThingSpeak
    msg_to_send = {'field1':temp, 'field2':humidity,'field3':x,'field5':ldr_value, 'field4':windspeed}
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = msg_to_send, headers = HTTP_HEADERS )  
    print('Données envoyées')
    request.close()
    led_net.value(0)
    time.sleep(2)
    led_net.value(1)
led_rp.value(0)
led_net.value(0)


