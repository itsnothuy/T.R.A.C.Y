import torchaudio

waveform, sample_rate = torchaudio.load("assistant_reply.wav")
print(waveform.shape)  # Should show (1, N) where N > 0

if waveform.abs().max() == 0:
    print("The WAV file is silent!")
else:
    print("The WAV file contains audio!")



