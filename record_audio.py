import pyaudio
import wave

chunk = 4096  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
filename = "output1.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

try:
    # Initialize array to store frames
    with wave.open(filename, 'wb') as f:
        f.setnchannels(channels)
        f.setsampwidth(p.get_sample_size(sample_format))
        f.setframerate(fs)

        while True:
            data = stream.read(4096)
            f.writeframes(bytes(data))
except KeyboardInterrupt:
    print("Stop recording...")
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
# Stop and close the stream


print('Finished recording')

