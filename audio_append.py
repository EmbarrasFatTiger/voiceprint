# encoding=utf-8

import librosa
import sox
import os
import numpy as np

cbn = sox.Combiner()
files_path = 'G:/data_calss/'
save_path = 'G:/wav_520/'
speaker = os.listdir(files_path)

for i in range(len(speaker)):
    front_list = []
    back_list = []
    small_s = files_path+speaker[i]+'/'

    if not os.path.exists(save_path+speaker[i]+'/'):
        savefile_path = os.makedirs(save_path+speaker[i]+'/')
    savefile_path = save_path+speaker[i]+'/'

    if not os.path.exists(savefile_path + 'ori' + '/'):
        savefile_path1 = os.makedirs(savefile_path + 'ori' + '/')
    savefile_path1 = savefile_path + 'ori' + '/'

    if not os.path.exists(savefile_path + 'noise' + '/'):
        savefile_path2 = os.makedirs(savefile_path + 'noise' + '/')
    savefile_path2 = savefile_path + 'noise' + '/'

    filepath = os.listdir(small_s)
    files = [small_s + sfile for sfile in filepath]
    k = 0
    for j in range(0, len(files)-50, 50):
        wav_list = files[j:j+50]

        cbn.convert(samplerate=16000, n_channels=1, )
        pathname = savefile_path1 + speaker[i] + str(k) + '.wav'
        try:
            cbn.build(wav_list, pathname, 'concatenate')
        except:
            continue
        print(speaker[i] + str(k) + '.wav')

        data, fs = librosa.core.load(pathname)
        rn = np.random.normal(0, 1, len(data))
        voice_noise = np.where(data != 0.0, data.astype('float64') + 0.002 * rn, 0.0).astype(np.float32)
        librosa.output.write_wav(savefile_path2 + speaker[i] + str(k) + '_noise.wav', voice_noise, fs)
        print(speaker[i] + str(k) + '_noise.wav')

        k += 1
