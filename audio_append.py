# encoding=utf-8
# from pydub import AudioSegment
#
# #AudioSegment.converter = 'D:\\PychramWork\\voice_dataextract\\ffmpeg-20190219-ff03418-win64-static\\bin\\ffmpeg.exe'
# song = AudioSegment.from_wav('D:/PychramWork/voice_dataextract/sound1.wav')

import sox
import os
cbn = sox.Combiner()
files_path = 'H:/temp/'
save_path = 'H:/save/'
speaker = os.listdir(files_path)
for i in range(len(speaker)):
    front_list = []
    back_list = []
    small_s = files_path+speaker[i]+'/'
    if not os.path.exists(save_path+speaker[i]+'/'):
        savefile_path = os.makedirs(save_path+speaker[i]+'/')
    savefile_path = save_path+speaker[i]+'/'
    filepath = os.listdir(small_s)
    files = [small_s + sfile for sfile in filepath]
    for j in range(0, len(files)-50, 50):
        front_list = files[j:j+50]
        #print(front_list)
    #back_list=files[100:200]
        print(savefile_path)
        cbn.convert(samplerate=16000, n_channels=1, )
        cbn.build(front_list, savefile_path + speaker[i] + str(j) + '.wav', 'concatenate')
        #cbn.build(back_list, savefile_path + speaker[i] + '_back.wav', 'concatenate')