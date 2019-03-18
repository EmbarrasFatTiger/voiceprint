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


def register():
    speakerId_list = ['vabcl_regis.wav', 'vabxi_regis.wav', 'vabxo_regis.wav', 'vabxr_regis.wav', 'vacvd_regis.wav',
                      'vacvj_regis.wav', 'vacvk_regis.wav', 'vacvp_regis.wav', 'vacvr_regis.wav', 'vadbj_regis.wav',
                      'vafxd_regis.wav', 'vafzh_regis.wav', 'vagab_regis.wav', 'vagan_regis.wav', 'vagas_regis.wav',
                      'vahrb_regis.wav', 'vahrk_regis.wav', 'vahrt_regis.wav', 'vaiwt_regis.wav', 'vaiwx_regis.wav',
                      'valor_regis.wav', 'vanso_regis.wav', 'vanzr_regis.wav', 'vaobb_regis.wav', 'vaokz_regis.wav',
                      'vaowg_regis.wav', 'vapmc_regis.wav', 'vapmu_regis.wav', 'vaqfu_regis.wav', 'vaqyc_regis.wav',
                      'vaqyj_regis.wav', 'vaqyv_regis.wav', 'vaszj_regis.wav', 'vatnl_regis.wav', 'vatno_regis.wav',
                      'vatnx_regis.wav', 'vauaq_regis.wav', 'vauid_regis.wav', 'vauij_regis.wav', 'vauix_regis.wav',
                      'vawau_regis.wav', 'vawhj_regis.wav', 'vaxle_regis.wav', 'vaxll_regis.wav', 'vaxlv_regis.wav',
                      'vaxsk_regis.wav', 'vaxsm_regis.wav', 'vbacl_regis.wav', 'vbdbc_regis.wav', 'vbdbh_regis.wav',
                      'vbdym_regis.wav', 'vbdyo_regis.wav', 'vbdyp_regis.wav', 'vbdyz_regis.wav', 'vbdzo_regis.wav',
                      'vbdzq_regis.wav', 'vbepf_regis.wav', 'vbfzp_regis.wav', 'vbgnb_regis.wav', 'vbgux_regis.wav',
                      'vbgyq_regis.wav', 'vbhkc_regis.wav', 'vbhke_regis.wav', 'vbhkf_regis.wav', 'vbhkh_regis.wav',
                      'vbhks_regis.wav', 'vbhvd_regis.wav', 'vbhvs_regis.wav', 'vbhvt_regis.wav', 'vbilo_regis.wav',
                      'vbjsa_regis.wav', 'vbkpc_regis.wav', 'vbkpy_regis.wav', 'vbktr_regis.wav', 'vbnci_regis.wav',
                      'vbnck_regis.wav', 'vbnvx_regis.wav', 'vcctk_regis.wav', 'vceen_regis.wav', 'vcfaw_regis.wav',
                      'vcffg_regis.wav', 'vcffm_regis.wav', 'vdbwt_regis.wav', 'vderc_regis.wav', 'vdgvt_regis.wav',
                      'vdpss_regis.wav', 'vdrvj_regis.wav', 'veamh_regis.wav', 'vecyw_regis.wav', 'vedtp_regis.wav',
                      'vedzt_regis.wav', 'veeuc_regis.wav', 'veglw_regis.wav', 'vegwm_regis.wav', 'vfcci_regis.wav',
                      'vfdnc_regis.wav', 'vfdnh_regis.wav', 'vfetp_regis.wav', 'vflex_regis.wav', 'vhhap_regis.wav']
    dir = r'/data/voiceprint_pressure_test_records/records/test/registered/'
    for name in speakerId_list:
        os.system('curl "http://192.168.99.214:19001/register?filename=' + dir + name + '"')


def test2speakers(local_path, remote_path, n):
    start_time = datetime.now()
    all_list = os.listdir(local_path)

    # print(len(all_list))
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
    remote_time_list = []

    for i in range(n):
        test2_list = sample(all_list, 2)
        true_list1 = sample(test2_list, 1)
        another_list = list(set(test2_list) - set(true_list1))
        wav_list.append(true_list1[0])

        true_name = true_list1[0][:5] + '_regis'
        another_name = another_list[0][:5] + '_regis'
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

        remote_time1 = datetime.now()
        RemoteScp(local_path, remote_path, wav_list)
        remmote_time2 = datetime.now()
        remote_time_list.append((remmote_time2 - remote_time1).total_seconds())
        # all_list = list(set(all_list).difference(set(wav_list)))
    end_time = datetime.now()
    remote_time = sum(remote_time_list)
    total_time = (end_time-start_time).total_seconds() - remote_time
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
    file_path = r'/home/voiceprint_acc_test/log2speakers_noise_' + time1 + '.xlsx'
    writer = pd.ExcelWriter(file_path)
    df = pd.DataFrame(dit)
    df.to_excel(writer, columns=['wav', 'actual_name', 'predicted_name', 'candidate1', 'candidate2', 'time',
                                 'null_number', 'total_time', 'acc1', 'acc2'], index=False, encoding='utf-8',
                sheet_name='2Speakers_' + str(n), float_format='%.6f')
    writer.save()


def test3speakers(local_path, remote_path, n):
    start_time = datetime.now()
    all_list = os.listdir(local_path)
    # print(len(all_list))
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
    remote_time_list = []
    k = 0
    for i in range(n):
        test3_list = sample(all_list, 3)
        true_list1 = sample(test3_list, 1)
        another_list = list(set(test3_list) - set(true_list1))
        wav_list.append(true_list1[0])

        true_name = true_list1[0][:5] + '_regis'
        candidate2 = another_list[0][:5] + '_regis'
        candidate3 = another_list[1][:5] + '_regis'
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

        remote_time1 = datetime.now()
        RemoteScp(local_path, remote_path, wav_list)
        remmote_time2 = datetime.now()
        remote_time_list.append((remmote_time2 - remote_time1).total_seconds())

        # all_list = list(set(all_list).difference(set(wav_list)))
    end_time = datetime.now()
    remote_time = sum(remote_time_list)
    total_time = (end_time - start_time).total_seconds() - remote_time
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
    file_path = r'/home/voiceprint_acc_test/log3speakers_noise_' + time1 + '.xlsx'
    writer = pd.ExcelWriter(file_path)
    df = pd.DataFrame(dit)
    df.to_excel(writer, columns=['wav', 'actual_name', 'predicted_name', 'candidate1', 'candidate2', 'candidate3',
                                 'time', 'null_number', 'total_time', 'acc1', 'acc2'], index=False, encoding='utf-8',
                sheet_name='3Speakers_' + str(n), float_format='%.6f')
    writer.save()


if __name__ == '__main__':
    test2speakers('/home/voiceprint_acc_test/verify/', '/data/voiceprint_pressure_test_records/records/test/verify/', 10)
    # test3speakers('/home/verify', '/data/voiceprint_pressure_test_records/records/test/verify/', 10)
