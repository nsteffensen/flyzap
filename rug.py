from gpiozero import LED, Button
from time import sleep, strftime
from subprocess import *
import lcddriver
from signal import pause
import pyaudio
import audioop

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE = 0  # This is specfic to RPi Zero W with USB mic

# LED setup
blueLed = LED(17)
redLed = LED(22)
blueLed.off()
redLed.off()

# Button setup
blueButton = Button(27)
redButton = Button(24)
clicks = 0
# startTime = 

# LCD setup
lcd = lcddriver.lcd()
lcd.lcd_clear()

def blueClicked():
    global clicks
    print('Counter: {}'.format(clicks))
    clicks += 1
    lcd.lcd_display_string(strftime('Zaps: {}'.format(clicks)), 1)

def redClicked():
    redLed.on()
    sleep(0.25)
    redLed.off()

blueButton.when_pressed = blueClicked
blueButton.when_released = blueLed.off
redButton.when_pressed = redClicked

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index = DEVICE)

print("Starting, use Ctrl+C to stop")

while True:
    data  = stream.read(CHUNK, False)  # read(num_frames, exception_on_overflow=True)
    rms   = audioop.rms(data, 2)  # shows volume
    if (rms > 100):
        print(rms)
        blueLed.on()
        sleep(0.1)
        blueLed.off()
        blueClicked()

