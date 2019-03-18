import librosa
import numpy as np
import os
voice_files_path = os.listdir('D:/sum/verify/')
# print(voice_files_path)


def addnoise_process(voice_file):
    data, fs = librosa.core.load('D:/sum/verify/' + voice_file)
    rn = np.random.normal(0, 1, len(data))
    voice_noise = np.where(data != 0.0, data.astype('float64') + 0.002 * rn, 0.0).astype(np.float32)
    librosa.output.write_wav('D:/sum/noise_verify/' + voice_file, voice_noise, fs)


for voice_file in voice_files_path:
    addnoise_process(voice_file)
