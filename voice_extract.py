import os
import sox
from pydub import AudioSegment as aug
import shutil
import re


def sph2wav(sph):
    def f1():
        tfm = sox.Transformer()
        try:
            tfm.build(sph, 'D:/sum/short3_wav/'+os.path.splitext(sph)[0].split('/')[-1] + '.wav')
            print(sph + ' is ok.')
        except Exception as e:
            print(e)

    def f2():
        try:
            os.system('sox ' + sph + ' D:/sum/short3_wav1/' + os.path.splitext(sph)[0].split('/')[-1] + '.wav')
            print(sph+' is ok.')
        except Exception as e:
            print(e)
    f2()


def extracwav(sound, start_end, filename):
    i = 0
    for time in start_end:
        sound[float(time[0]) * 1000:float(time[1]) * 1000].export(r'D:/sum/short3_final/'+filename+r'/' + filename + str(i) + '.wav', 'wav')
        i += 1


def aaa():
    key_file = 'D:/2008_nist_sre_te_LDC2011S08/2008_nist_sre_te/data/keys/NIST_SRE08_KEYS.v0.1/segment-keys/' \
               'test/NIST_SRE08_short3.test.segment.key'
    segID_list = []
    speaker_ID = []
    with open(key_file, 'r') as f:
        k_file = f.readlines()
        for line in k_file[1:]:
            details = line.strip().split(',')
            seg_ID = details[0]
            speaker_ID = details[-1].split(':')[0]
            segID_list.append(seg_ID)
            speaker_ID.append(s_Id)

    wavdata = r'D:/sum/short3_final/'
    for line in k_file.readlines()[1:]:
        formatline = line.strip()
        seg_ID = formatline[0:5]
        s_Id = formatline.split(',')[-1][0:6]
        # if s_Id in speaker_ID:
        #     continue

    print(segID_list)
    datadir = r'D:/sum/short3_wav/'
    vad_dir = r'D:/2008_nist_sre_te_LDC2011S08/2008_nist_sre_te/data/vad/test/short3/'
    for filename in segID_list:
        # sph2wav(filename)
        class_dir = r'D:/sum/short3_final/'+filename+'/'
        if os.path.exists(class_dir):
            continue
        vadlist = []
        vadfile = open(vad_dir+filename+'.vad')
        os.makedirs(class_dir)
        for vadline in vadfile.readlines():
            formatvadline = vadline.strip()
            splitline = formatvadline.split(' ')
            vadlist.append([float(splitline[2]), float(splitline[4])])
            #print(wavdata+filename+'.wav')
            sound = aug.from_wav(wavdata+filename+'.wav')
        print(vadlist)
        extracwav(sound, vadlist, filename)


def short3_sph2wav_main():
    name2_list = []
    with open('D:/short3_vad.txt', 'r') as f:
        for name2 in f.readlines():
            name2_list.append(name2.strip())
    # print(name2_list)
    for name in name2_list:
        name1 = 'D:/2008_nist_sre_te_LDC2011S08/2008_nist_sre_te/data/vad/test/short3/'+name+'.vad'
        if not os.path.exists(name1):
            print(name1 + ' does not exist.')
        else:
            shutil.copy(name1, 'E:/Newdataset/short3vad/')


def select_vad_main():
    vad_list = []
    with open('D:/short3_vad.txt', 'r') as f:
        vad_list1 = f.readlines()
        for name in vad_list1:
            vad_list.append(name.strip())
    k_list = []
    with open('D:/2008_nist_sre_te_LDC2011S08/2008_nist_sre_te/data/keys/NIST_SRE08_KEYS.v0.1/segment-keys/test/'
              'NIST_SRE08_short3.test.segment.key', 'r') as k:
        key = k.readlines()
        for name in key:
            k_list.append(name.strip())
    with open('E:/Newdataset/short3key.txt', 'w') as w:
        for name in vad_list:
            for key_content in key:
                try:
                    if re.findall(name, key_content):
                        w.write(key_content)
                        print(name + 'write success.')
                    # else:
                    #     print(name + ' does not exist.')
                except Exception as e:
                    print(e)


def cut_wav():
    # key文件
    with open('E:/Newdataset/short3key/short3key.txt', 'r') as f:
        key_content = f.readlines()

    # wav文件存储路径
    wav_dir = 'E:/Newdataset/short3wav/'
    wav_list = os.listdir(wav_dir)
    # print(wav_list)

    # vad文件存储路径
    vad_dir = 'E:/Newdataset/short3vad/'
    vad_list = os.listdir(vad_dir)
    # print(vad_list)

    # 首先提取vad中的秒数
    for i in range(0, len(vad_list)):
        # 将所有的起止时间存储到time列表里边
        with open(vad_dir + vad_list[i], 'r') as a:
            lines = a.readlines()
            time = []
            for j in range(lines.__len__()):
                split = lines[j].split(' ')
                time.append([split[2], split[4].strip('\n')])
            #
            # print(time)
            # print(type(float(time[4][1])))

            # 判断vad文件名和wav文件名是否一致
            if vad_list[i].split('.')[0] == wav_list[i].split('.')[0]:
                # 加载wav文件
                sound = aug.from_wav(wav_dir + wav_list[i])
                for name in key_content:
                    if re.findall(wav_list[i][0:5], name):
                        speaker_id = name.split(',')[-1][0:6]
                        if not os.path.exists('E:/short3wav/'+speaker_id+'/'):
                            os.makedirs('E:/short3wav/'+speaker_id+'/')
                        cut_dir = 'E:/short3wav/'+speaker_id+'/'
                        if not os.path.exists('E:/Newdataset/short3wav_c1r16/'+speaker_id+'/'):
                            os.makedirs('E:/Newdataset/short3wav_c1r16/'+speaker_id+'/')
                        save_dir = 'E:/Newdataset/short3wav_c1r16/'+speaker_id+'/'

                # 设置空的音频
                playlist = aug.empty()

                # 按照列表中的时间截取并拼合音频
                for k in range(0, time.__len__()):
                    playlist += sound[float(time[k][0]) * 1000: float(time[k][1]) * 1000]
                # 输出音频
                playlist.export(cut_dir + wav_list[i], format='wav')
                # os.system('sox ' + cut_dir + wav_list[i] + ' -c1 -r16000 ' + save_dir + wav_list[i])
                print(wav_list[i] + ' ok')
            else:
                print('++++++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    list1 = ['101981', '102473', '102725', '103137', '103582', '103623', '103646', '103872', '104165', '104747', '105477', '106236', '106453', '106828', '107383', '108144', '109786', '110074', '110085', '110092', '110099', '110100', '110103', '110104', '110111', '110112', '110115', '110116', '110118', '110130', '110137', '110157', '110163', '110165', '110204', '110207', '110211', '110214', '110233', '110238', '110245', '110251', '110264', '110275', '110279', '110281', '110283', '110290', '110295', '110298', '110299', '110310', '110322', '110333', '110338', '110372', '110385', '110386', '110392', '110396', '110400', '110401', '110403', '110404', '110405', '110407', '110413', '110422', '110430', '110432', '110440', '110453', '110456', '110461', '110463', '110464', '110465', '110469', '110476', '110478', '110479', '110490', '110513', '110515', '110519', '110522', '110525', '110532', '110538', '110541', '110548', '110550', '110552', '110558', '110559', '110567', '110568', '110569', '110578', '110579', '110580', '110582', '110587', '110591', '110592', '110594', '110608', '110609', '110618', '110621', '110623', '110625', '110626', '110633', '110655', '110656', '110657', '110664', '110665', '110673', '110752', '110768', '110770', '110779', '110780', '110803', '110806', '110807', '110808', '110879', '111052', '111081', '111167', '111178', '111218', '111263', '111319', '111332', '111340', '111374', '111380', '111400', '111405', '111409', '111416', '111445', '111469', '111506', '111513', '111563']
    list2 = ['101981', '102473', '102725', '103137', '103582', '103623', '103646', '103872', '104165', '104747', '105477', '106236', '106453', '106828', '107383', '108144', '109786', '110074', '110085', '110092', '110099', '110100', '110103', '110104', '110111', '110112', '110115', '110116', '110118', '110130', '110137', '110157', '110163', '110165', '110204', '110207', '110211', '110214', '110233', '110238', '110245', '110251', '110264', '110275', '110279', '110281', '110283', '110290', '110295', '110298', '110299', '110310', '110322', '110333', '110338', '110372', '110385', '110386', '110392', '110396', '110400', '110401', '110403', '110404', '110405', '110407', '110413', '110422', '110430', '110432', '110440', '110453', '110456', '110461', '110463', '110464', '110465', '110469', '110476', '110478', '110479', '110490', '110513', '110515', '110519', '110522', '110525', '110532', '110538', '110541', '110548', '110550', '110552', '110558', '110559', '110567', '110568', '110569', '110578', '110579', '110580', '110582', '110587', '110591', '110592', '110594', '110608', '110609', '110618', '110621', '110623', '110625', '110626', '110633', '110655', '110656', '110657', '110664', '110665', '110673', '110752', '110768', '110770', '110779', '110780', '110803', '110806', '110807', '110808', '110879', '111052', '111081', '111167', '111178', '111218', '111263', '111319', '111332', '111340', '111374', '111380', '111400', '111405', '111409', '111416', '111445', '111469', '111506', '111513', '111563']
    list3 = ['101981', '102473', '102725', '103137', '103582', '103623', '103646', '103872', '104165', '104747', '105477', '106236', '106453', '106828', '107383', '108144', '109786', '110074', '110085', '110092', '110099', '110100', '110103', '110104', '110111', '110112', '110115', '110116', '110118', '110130', '110137', '110157', '110163', '110165', '110204', '110207', '110211', '110214', '110233', '110238', '110245', '110251', '110264', '110275', '110279', '110281', '110283', '110290', '110295', '110298', '110299', '110310', '110322', '110333', '110338', '110372', '110385', '110386', '110392', '110396', '110400', '110401', '110403', '110404', '110405', '110407', '110413', '110422', '110430', '110432', '110440', '110453', '110456', '110461', '110463', '110464', '110465', '110469', '110476', '110478', '110479', '110490', '110513', '110515', '110519', '110522', '110525', '110532', '110538', '110541', '110548', '110550', '110552', '110558', '110559', '110567', '110568', '110569', '110578', '110579', '110580', '110582', '110587', '110591', '110592', '110594', '110608', '110609', '110618', '110621', '110623', '110625', '110626', '110633', '110655', '110656', '110657', '110664', '110665', '110673', '110752', '110768', '110770', '110779', '110780', '110803', '110806', '110807', '110808', '110879', '111052', '111081', '111167', '111178', '111218', '111263', '111319', '111332', '111340', '111374', '111380', '111400', '111405', '111409', '111416', '111445', '111469', '111506', '111513', '111563']
    print(len(list1), len(list2), len(list3))