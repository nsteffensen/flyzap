import pyaudio
import audioop

# http://people.csail.mit.edu/hubert/pyaudio/docs/

# chunk      = 2**11 # Change if too fast/slow, never less than 2**11
# scale      = 50    # Change if too dim/bright
# exponent   = 5     # Change if too little/too much difference between loud and quiet sounds
# samplerate = 44100 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# CHANGE THIS TO CORRECT INPUT DEVICE
# Enable stereo mixing in your sound card
# to make you sound output an input
# Use list_devices() to list all your input devices
# DEVICE   = 2  # I think this works on the PC
DEVICE   = 0  # I think this works on the RPi Zero W
 

p = pyaudio.PyAudio()
# stream = p.open(format = pyaudio.paInt16,
#                 channels = 1,
#                 rate = 44100,
#                 input = True,
#                 frames_per_buffer = chunk,
#                 input_device_index = device)

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

    # level = min(rms / (2.0 ** 16) * scale, 1.0) 
    # level = level**exponent 
    # level = int(level * 255)

    # print level