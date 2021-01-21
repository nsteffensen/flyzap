import pyaudio
import audioop
from gpiozero import LED, Button
from time import sleep, strftime, time
from subprocess import *
import lcddriver
from signal import pause
import wave

#------------------------------------------------------------------------------
clicks = 0

#------------------------------------------------------------------------------
blueLed = LED(17)
redLed = LED(22)
blueLed.off()
redLed.off()
blueButton = Button(27)
redButton = Button(24)
lcd = lcddriver.lcd()
lcd.lcd_clear()

# def blueClicked():
#     global clicks
#     global startTime
#     print('Counter: {}'.format(clicks))
#     clicks += 1
#     lcd.lcd_display_string(strftime('Zaps: {}'.format(clicks)), 1)
#     now = time()
#     hours, rem = divmod(now-startTime, 3600)
#     minutes, seconds = divmod(rem, 60)
#     # lcd.lcd_display_string(strftime("Up: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)), 2)
#     lcd.lcd_display_string(strftime("Up: {:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds))), 2)

def redClicked():
    redLed.on()
    sleep(0.25)
    redLed.off()



#------------------------------------------------------------------------------
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE = 0  # RPi Zero W
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"


def blueClicked():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index = DEVICE)

    lcd.lcd_display_string(strftime('Start rec...'), 2)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

    lcd.lcd_display_string(strftime('End rec...'), 2)

    stream.stop_stream()
    stream.close()
    p.terminate()

    now = time()
    hours, rem = divmod(now, 3600)
    minutes, seconds = divmod(rem, 60)
    outfile = "rec_{:0>2}-{:0>2}-{:0>2}.wav".format(int(hours),int(minutes),int(seconds))
    wf = wave.open(outfile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    lcd.lcd_display_string(strftime('File written.'), 2)
    time.sleep(2)
    lcd.lcd_display_string(strftime(''), 2)

#------------------------------------------------------------------------------
blueButton.when_pressed = blueClicked
blueButton.when_released = blueLed.off
redButton.when_pressed = redClicked

lcd.lcd_display_string(strftime('Recording Util'), 1)
