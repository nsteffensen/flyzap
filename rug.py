from gpiozero import LED, Button
from time import sleep, strftime, time
from subprocess import *
import lcddriver
from signal import pause
import pyaudio
# from datetime import datetime
from detectZap import fullFft, justRms

# startTime = datetime.now()
startTime = time()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE = 0  # This is specfic to RPi Zero W with USB mic

#------------------------------------------------------------------------------
# LED setup
blueLed = LED(17)
redLed = LED(22)
blueLed.off()
redLed.off()

#------------------------------------------------------------------------------
# LCD setup
lcd = lcddriver.lcd()
lcd.lcd_clear()

#------------------------------------------------------------------------------
def blueClicked():
    global clicks
    global startTime
    print('Counter: {}'.format(clicks))
    clicks += 1
    lcd.lcd_display_string(strftime('Zaps: {}'.format(clicks)), 1)
    now = time()
    hours, rem = divmod(now-startTime, 3600)
    minutes, seconds = divmod(rem, 60)
    # lcd.lcd_display_string(strftime("Up: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)), 2)
    lcd.lcd_display_string(strftime("Up: {:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds))), 2)

#------------------------------------------------------------------------------
def redClicked():
    redLed.on()
    sleep(0.25)
    redLed.off()

#------------------------------------------------------------------------------
# Button setup
blueButton = Button(27)
redButton = Button(24)
clicks = 0

blueButton.when_pressed = blueClicked
blueButton.when_released = blueLed.off
redButton.when_pressed = redClicked

#------------------------------------------------------------------------------
# Main loop
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
    # rms   = audioop.rms(data, 2)  # shows volume
    # if (rms > 100):
    rmsThreshold = 100
    fftThreshold = 1000
    # zap = justRms(data, rmsThreshold)
    zap = fullFft(data, fftThreshold)
    if (zap):
        # print(rms)
        blueLed.on()
        sleep(0.1)
        blueLed.off()
        blueClicked()

