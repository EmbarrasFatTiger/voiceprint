# coding=<utf-8>
import os
import shutil
import time
from datetime import datetime
import pandas as pd
from random import sample
from sklearn.metrics import accuracy_score
import paramiko


def RemoteScp(local_path, remote_path, wav_list):
    host_ip = '192.168.99.214'
    host_port = 22
    host_username = 'root'
    host_password = 'echoServer!@#'

    ssh = paramiko.Transport((host_ip, host_port))
    ssh.connect(username=host_username, password=host_password)
    sftp = paramiko.SFTPClient.from_transport(ssh)

    try:
        # remote_files = sftp.listdir(remote_path)
        for file in wav_list:
            local_file = local_path + file
            remote_file = remote_path + file
            sftp.put(local_file, remote_file)
    except IOError as err:
        return err
    ssh.close()


def register(remote_path):
    speakerId_list = []
    with open('read_list.txt', 'r') as f:
        for line in f.readlines():
            speakerId_list.append(line.strip('\n'))
    for name in speakerId_list:
        os.system('curl "http://192.168.99.214:19001/register?filename=' + remote_path + name + '"')
        # print('curl "http://192.168.99.214:19001/register?filename=' + remote_path + name + '"')


def test2speakers(remote_path, n):
    all_list = []
    with open('read_list.txt', 'r') as f:
        for line in f.readlines():
            all_list.append(line.strip('\n'))
    start_time = datetime.now()
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    actual_result_list = []  # Save actual results
    real_actual_result_list = []
    pred_result_list = []  # Save predicted results
    wav_list = []  # Save the extracted elements
    during_time = []
    all_another_list = []
    k_list = []
    total_time_list = []
    acc_list = []
    acc_null_list = []
    k = 0
    # remote_time_list = []

    for i in range(n):
        test2_list = sample(all_list, 2)
        true_list1 = sample(test2_list, 1)
        another_list = list(set(test2_list) - set(true_list1))
        wav_list.append(true_list1[0])

        true_name = true_list1[0][:5] + '_regis_noise'
        another_name = another_list[0][:5] + '_regis_noise'
        all_another_list.append(another_name)
        pred_result_list.append(true_name)

        starttime = datetime.now()
        result = os.popen('curl "http://192.168.99.214:19001/recognize?filename=' + remote_path + true_list1[0] +
                          "&ranges=" + true_name + '%7C' + another_name + '"')
        res = result.read()
        endtime = datetime.now()
        if len(res) == 0:
            actual_result_list.append(true_name)
            k += 1
        else:
            actual_result_list.append(res)

        real_actual_result_list.append(res)
        during_time.append((endtime - starttime).total_seconds())

        # remote_time1 = datetime.now()
        # RemoteScp(local_path, remote_path, wav_list)
        # remmote_time2 = datetime.now()
        # print(remmote_time2 - remote_time1)
        # remote_time_list.append((remmote_time2 - remote_time1).total_seconds())
        all_list = list(set(all_list).difference(set(wav_list)))
    end_time = datetime.now()
    # remote_time = sum(remote_time_list)
    # total_time = (end_time-start_time).total_seconds() - remote_time
    total_time = (end_time - start_time).total_seconds()
    acc = accuracy_score(pred_result_list, actual_result_list)
    acc_null = accuracy_score(pred_result_list, real_actual_result_list)
    acc_null_list.append(acc_null)
    total_time_list.append(total_time)
    k_list.append(k)
    acc_list.append(acc)

    for i in range(len(pred_result_list) - 1):
        k_list.append(' ')
        total_time_list.append(' ')
        acc_list.append(' ')
        acc_null_list.append(' ')

    dit = {'wav': wav_list, 'actual_name': pred_result_list, 'predicted_name': real_actual_result_list,
           'candidate1': pred_result_list, 'candidate2': all_another_list, 'time': during_time, 'null_number':
               k_list, 'total_time': total_time_list, 'acc1': acc_list, 'acc2': acc_null_list}
    file_path = r'/home/voiceprint_acc_test/2speakers_3_' +str(n)+'_'+ time1 + '.xlsx'
    writer = pd.ExcelWriter(file_path)
    df = pd.DataFrame(dit)
    df.to_excel(writer, columns=['wav', 'actual_name', 'predicted_name', 'candidate1', 'candidate2', 'time',
                                 'null_number', 'total_time', 'acc1', 'acc2'],
                index=False, encoding='utf-8', sheet_name='2Speakers_' + str(n), float_format='%.6f')
    writer.save()


def test3speakers(remote_path, n):
    all_list = []
    with open('read_list.txt', 'r') as f:
        for line in f.readlines():
            all_list.append(line.strip('\n'))
    start_time = datetime.now()
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))

    actual_result_list = []  # Save actual results
    real_actual_result_list = []
    pred_result_list = []  # Save predicted results
    wav_list = []  # Save the extracted elements
    during_time = []
    all_another_list1 = []
    all_another_list2 = []
    k_list = []
    total_time_list = []
    acc_list = []
    acc_null_list = []
    # remote_time_list = []
    k = 0
    for i in range(n):
        test3_list = sample(all_list, 3)
        true_list1 = sample(test3_list, 1)
        another_list = list(set(test3_list) - set(true_list1))
        wav_list.append(true_list1[0])

        true_name = true_list1[0][:5] + '_regis_noise'
        candidate2 = another_list[0][:5] + '_regis_noise'
        candidate3 = another_list[1][:5] + '_regis_noise'
        all_another_list1.append(candidate2)
        all_another_list2.append(candidate3)
        pred_result_list.append(true_name)

        starttime = datetime.now()
        result = os.popen('curl "http://192.168.99.214:19001/recognize?filename=' + remote_path + true_list1[0] +
                          "&ranges=" + true_name + '%7C' + candidate2 + '%7C' + candidate3 + '"')
        res = result.read()
        endtime = datetime.now()

        if len(res) == 0:
            actual_result_list.append(true_name)
            k += 1
        else:
            actual_result_list.append(res)
        real_actual_result_list.append(res)
        during_time.append((endtime - starttime).total_seconds())

        # remote_time1 = datetime.now()
        # RemoteScp(local_path, remote_path, wav_list)
        # remmote_time2 = datetime.now()
        # remote_time_list.append((remmote_time2 - remote_time1).total_seconds())

        all_list = list(set(all_list).difference(set(wav_list)))
    end_time = datetime.now()
    # remote_time = sum(remote_time_list)
    # total_time = (end_time - start_time).total_seconds() - remote_time
    total_time = (end_time - start_time).total_seconds()
    acc = accuracy_score(pred_result_list, actual_result_list)
    acc_null = accuracy_score(pred_result_list, real_actual_result_list)

    acc_null_list.append(acc_null)
    total_time_list.append(total_time)
    k_list.append(k)
    acc_list.append(acc)

    for i in range(len(pred_result_list) - 1):
        k_list.append(' ')
        total_time_list.append(' ')
        acc_list.append(' ')
        acc_null_list.append(' ')

    dit = {'wav': wav_list, 'actual_name': pred_result_list, 'predicted_name': real_actual_result_list,
           'candidate1': pred_result_list, 'candidate2': all_another_list1, 'candidate3': all_another_list2, 'time':
            during_time, 'null_number': k_list, 'total_time': total_time_list, 'acc1': acc_list, 'acc2': acc_null_list}
    file_path = r'/home/voiceprint_acc_test/3speakers_3_' +str(n)+'_'+ time1 + '.xlsx'
    writer = pd.ExcelWriter(file_path)
    df = pd.DataFrame(dit)
    df.to_excel(writer, columns=['wav', 'actual_name', 'predicted_name', 'candidate1', 'candidate2', 'candidate3',
                                 'time', 'null_number', 'total_time', 'acc1', 'acc2'], index=False, encoding='utf-8',
                sheet_name='3Speakers_' + str(n), float_format='%.6f')
    writer.save()


if __name__ == '__main__':
    # register('/data/voiceprint_pressure_test_records/records/test/wanhejie_noise/regis_noise_6s/')
    test2speakers('/data/voiceprint_pressure_test_records/records/test/wanhejie_noise/verify3_noise/', 1200)
    # test3speakers('/data/voiceprint_pressure_test_records/records/test/verify6_9/', 4000)
