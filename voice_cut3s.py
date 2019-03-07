from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import shutil
path1 = r'G:/save16K/'
list1 = os.listdir(path1)
for i in range(len(list1)):
    path2 = path1 + list1[i] + '/'
    list2 = os.listdir(path2)
    path3 = path2 + list2[1]
    shutil.copyfile(path2 + list2[0], 'G:/test16K3s/' + list1[i] + '/' + list2[0][:-5] + '_regis.wav')
    # print(path3)
    myaudio = AudioSegment.from_file(path3, "wav")
    chunk_length_ms = 3000  # 分块的毫秒数
    chunks = make_chunks(myaudio, chunk_length_ms)  # 将文件切割成1秒每块

    # 保存切割的音频到文件

    for j, chunk in enumerate(chunks):
        chunk_name = (list2[1][:-5] + '{0}.wav').format(j)
        if not os.path.exists('G:/test16K3s/' + list1[i] + '/'):
            savefile_path = os.makedirs('G:/test16K3s/' + list1[i] + '/')
        savefile_path = 'G:/test16K3s/' + list1[i] + '/'
        # print(savefile_path+chunk_name + '  ' + list2[1])
        print("exporting", savefile_path + chunk_name)
        chunk.export(savefile_path + chunk_name, format="wav")