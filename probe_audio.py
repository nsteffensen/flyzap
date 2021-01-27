import pyaudio

# def check_rate(index, rate):
#     global p
#     devinfo = p.get_device_info_by_index(index)  # Or whatever device you care about.
#     if p.is_format_supported(rate,  # Sample rate
#                          input_device=devinfo['index'],
#                          input_channels=devinfo['maxInputChannels'],
#                          input_format=pyaudio.paInt16):
#         print 'Device index {} supports rate {}'.format(index, rate)


p = pyaudio.PyAudio()
devinfo = p.get_default_input_device_info()
name = devinfo['name']
rate = devinfo['defaultSampleRate']
print'Default input device {} has default sample rate of: {}'.format(name, rate)

