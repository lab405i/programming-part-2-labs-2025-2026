import time
from machine import Pin
from time import sleep

time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

LED_PIN = 15

led = Pin(LED_PIN, Pin.OUT)

while True:
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)
