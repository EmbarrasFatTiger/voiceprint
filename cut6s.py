from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import random


def cut6s(path):
    list1 = os.listdir(path)
    for i in range(len(list1)):
        filename = os.path.join(path, list1[i])
        # shutil.copyfile(path2 + list2[0], 'D:/addsum/' + list2[0][:-5] + '_regis.wav')
        # print(path3)
        myaudio = AudioSegment.from_file(filename, "wav")
        chunk_length_ms1 = 6000  # 分块的毫秒数
        chunks1 = make_chunks(myaudio, chunk_length_ms1)  # 将文件切割成6秒每块
        # chunks2 = make_chunks(myaudio, chunk_length_ms2)  # 将文件切割成6-9秒每块
        # print(len(chunks))
        # 保存切割的音频到文件

        # for k, chunk1 in enumerate(chunks1):
        # chunk_name = (list1[j][:-5] + '{0}.wav').format(k)
        chunk_name = filename
        # if not os.path.exists('G:/test16K3s/' + list1[i] + '/'):
        #     savefile_path = os.makedirs('G:/test16K3s/' + list1[i] + '/')
        savefile_path = '/data/voiceprint_pressure_test_records/records/test/registered-6s/'
        # print(savefile_path+chunk_name + '  ' + list2[1])
        print("exporting", savefile_path + chunk_name)
        chunks1[0].export(savefile_path + chunk_name, format="wav")

        # for l, chunk2 in enumerate(chunks2):
        #     chunk_name = (list2[j][:-5] + '{0}.wav').format(l)
        #     # if not os.path.exists('G:/test16K3s/' + list1[i] + '/'):
        #     #     savefile_path = os.makedirs('G:/test16K3s/' + list1[i] + '/')
        #     savefile_path = 'D:/addsum/'
        #     # print(savefile_path+chunk_name + '  ' + list2[1])
        #     print("exporting", savefile_path + chunk_name)
        #     chunk2.export(savefile_path + chunk_name, format="wav")

# path = r'D:/test16K3s/'
# name = os.listdir(path)
# print(name)
# # with open('speakerId.txt', 'w') as f:
# #     for name1 in name:
# #         f.write(name1+'\n')


if __name__ == '__main__':
    path = r'/data/voiceprint_pressure_test_records/records/test/registered/'
    cut6s(path)
