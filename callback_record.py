import pyaudio
# import audioop
from gpiozero import LED, Button
from time import sleep, strftime, time
from subprocess import *
import lcddriver
from signal import pause
import wave

#------------------------------------------------------------------------------
#  Set up
#------------------------------------------------------------------------------
blueLed = LED(17)
redLed = LED(22)
blueLed.off()
redLed.off()
blueButton = Button(27)
redButton = Button(24)
lcd = lcddriver.lcd()
lcd.lcd_clear()

def redClicked():
    redLed.on()
    sleep(0.25)
    redLed.off()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 44100  # First try. didn't seem to work
RATE = 48000  # Value returned by probe_audio
DEVICE = 0  # RPi Zero W
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

recording = False
recorded_frames = []

#------------------------------------------------------------------------------
#  Audio callback
#------------------------------------------------------------------------------
def audioCallback(in_data, frame_count, time_info, status):
    global recorded_frames
    if recording:
        recorded_frames.append(in_data)
        callback_flag = pyaudio.paContinue
    else:
        callback_flag = pyaudio.paComplete
    return (in_data, callback_flag)

#------------------------------------------------------------------------------
#  Record when button pressed
#------------------------------------------------------------------------------
def blueClickedCallback():
    global recorded_frames
    blueLed.on

    # Start recording
    lcd.lcd_display_string(strftime('Start rec...'), 2)
    recording = True
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=48000,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback = audioCallback)
                    
    # Sleep for duration desired for callback to record
    sleep(RECORD_SECONDS)

    # Stop recording and close stream
    recording = False
    blueLed.off
    lcd.lcd_display_string(strftime('End rec...'), 2)
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save data to files
    now = time()
    hours, rem = divmod(now, 3600)
    minutes, seconds = divmod(rem, 60)

    RAWFILE = True
    if RAWFILE == True:
        rawfile = "rec_{:0>2}-{:0>2}-{:0>2}.raw".format(int(hours),int(minutes),int(seconds))
        file = open(rawfile, "wb")
        file.write(b''.join(recorded_frames))
        file.close

    WAVFILE = True
    if WAVFILE == True:
        outfile = "rec_{:0>2}-{:0>2}-{:0>2}.wav".format(int(hours),int(minutes),int(seconds))
        wf = wave.open(outfile, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(recorded_frames))
        wf.close()

    lcd.lcd_display_string(strftime('File written.'), 2)
    sleep(2)
    lcd.lcd_display_string(strftime('               '), 2)

#------------------------------------------------------------------------------
#  Main
#------------------------------------------------------------------------------
blueButton.when_pressed = blueClicked
# blueButton.when_released = blueLed.off
redButton.when_pressed = redClicked

lcd.lcd_display_string(strftime('Recording Util'), 1)

while True:
    pause()  # This should be the right way to "do nothing"

