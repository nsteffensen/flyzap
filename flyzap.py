from gpiozero import LED, Button
from time import sleep, strftime
from subprocess import *
import lcddriver
from signal import pause

# LED setup
blue = LED(17)
red = LED(21)
blue.off()
red.off()

# Button setup
button = Button(27)
clicks = 0

# LCD setup
lcd = lcddriver.lcd()
lcd.lcd_clear()

def clicked():
    global clicks
    blue.on()
    print('Counter: {}'.format(clicks))
    clicks += 1
    lcd.lcd_display_string(strftime('Clicks: {}'.format(clicks)), 1)

button.when_pressed = clicked
# button.when_pressed = blue.on
button.when_released = blue.off

while True:
    red.on()
    sleep(1)
    red.off()
    sleep(1)

# pause()