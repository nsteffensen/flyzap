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
    print('Counter: {}'.format(clicks))
    clicks += 1
    lcd.lcd_display_string(strftime('Clicks: {}'.format(clicks)), 1)

button.when_pressed = clicked
# button.when_pressed = blue.on
button.when_released = blue.off

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
        blue.on()
        sleep(0.1)
        blue.off()
        clicked()

