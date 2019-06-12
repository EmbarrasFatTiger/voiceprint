# -*- coding:'utf-8' -*-
import os
import librosa
import numpy as np
from pydub import AudioSegment


def add_white_noise(voice_file):
    data, fs = librosa.core.load('D:/sum/registered/' + voice_file)
    rn = np.random.normal(0, 1, len(data))
    voice_noise = np.where(data != 0.0, data.astype('float64') + 0.002 * rn, 0.0).astype(np.float32)
    librosa.output.write_wav('D:/sum/noise_registered/' + voice_file[:-4] + '_noise.wav', voice_noise, fs)


def overlay_noise_wav(sound1, sound2):
    try:
        sound11 = AudioSegment.from_file(sound1)
        sound22 = AudioSegment.from_file(sound2)
    except Exception as e:
        print(e)
        return 'There is some wrong with ' + sound1
    k = 0
    while (sound11.dBFS - sound22.dBFS) < 20:
        sound22 = sound22.apply_gain(-3)
        k += 1
        if k >= 100:
            sound11 = sound11.apply_gain(3)



    print(sound1.split('\\')[-1], sound11.dBFS, sound22.dBFS, sound11.dBFS - sound22.dBFS)
    combined = sound11.overlay(sound22, loop=True).set_channels(1).set_frame_rate(16000).set_sample_width(2)
    return combined
    # combined.export("D:\\files\\new_noise\\" + sound1.split('\\')[-2]+'_'+sound1.split('\\')[-1][:-4]+'.wav', format='wav')


if __name__ == '__main__':
    noise0 = 'E:/Newdataset/0.wav'
    noise1 = 'E:/Newdataset/1.wav'
    noise2 = 'E:/Newdataset/2.wav'
    noise3 = 'E:/Newdataset/3.wav'
    noise4 = 'E:/Newdataset/4.wav'
    noise5 = 'E:/Newdataset/5.wav'
    noise6 = 'E:/Newdataset/6.wav'
    noise7 = 'E:/Newdataset/7.wav'
    noise = [noise0, noise1, noise2, noise3, noise4, noise5, noise6, noise7]
    path = 'E:\\Newdataset\\1nist\\'
    speaker_id = os.listdir(path)
    k = 1
    with open('D:\\files\\nist_noise.csv', 'w') as f:
        for i in range(len(speaker_id)):
            wav_path = os.path.join(path, speaker_id[i])
            wav_list = os.listdir(wav_path)
            for j in range(round(len(wav_list)/10)):
                wav = os.path.join(wav_path, wav_list[j])
                sound_after = overlay_noise_wav(wav, noise0)

                if not os.path.exists("D:\\files\\nist_nosie\\"+speaker_id[i]+'\\'):
                    os.makedirs("D:\\files\\nist_nosie\\"+speaker_id[i]+'\\')
                sound_after.export("D:\\files\\nist_nosie\\"+speaker_id[i]+'\\'+wav_list[j])
                sound_after2 = overlay_noise_wav("D:\\files\\nist_nosie\\"+speaker_id[i]+'\\'+wav_list[j], noise[k])
                # os.remove("D:\\files\\nist_nosie\\"+speaker_id[i]+'\\'+wav_list[j])
                sound_after2.export("D:\\files\\nist_nosie\\"+speaker_id[i]+'\\'+wav_list[j])
                print(speaker_id[i], wav_list[j], noise[k].split('/')[-1][0])
                f.write(speaker_id[i]+','+wav_list[j]+','+noise[0].split('/')[-1][0]+','+noise[k].split('/')[-1][0]+'\n')
                k += 1
                if k == 8:
                    k = 1


    # sound = AudioSegment.from_file(noise1)
    # sound1 = sound.apply_gain(-15)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/11.wav', format='wav')
    # sound = AudioSegment.from_file(noise2)
    # sound1 = sound.apply_gain(-15)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/22.wav', format='wav')
    # sound = AudioSegment.from_file(noise3)
    # sound1 = sound.apply_gain(-15)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/33.wav', format='wav')
    # sound = AudioSegment.from_file(noise4)
    # sound1 = sound.apply_gain(-10)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/44.wav', format='wav')
    # sound = AudioSegment.from_file(noise5)
    # sound1 = sound.apply_gain(-25)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/55.wav', format='wav')
    # sound = AudioSegment.from_file(noise6)
    # sound1 = sound.apply_gain(-20)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/66.wav', format='wav')
    # sound = AudioSegment.from_file(noise7)
    # sound1 = sound.apply_gain(-15)
    # print(sound1.dBFS)
    # sound1.export('E:/Newdataset/新数据集噪音/77.wav', format='wav')
