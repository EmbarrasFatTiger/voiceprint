# -*- coding: UTF-8 -*-
import os
import sys
from random import sample
import datetime
import pandas as pd
from sklearn.metrics import accuracy_score


def test2speakers(wav_txt, remote_path, n):
    """
    :param wav_txt: 远程音频列表txt
    :param remote_path: 远程音频所在的文件夹的路径
    :param n: 测试次数
    :return: 准确率excel文件
    """
    all_list = []  # 测试音频文件列表
    with open(wav_txt, 'r') as f:
        for line in f.readlines():
            all_list.append(line.strip('\n'))  # 先读取测试用例的文件名列表
    # 注册人列表
    register100 = ['vbdbh_regis', 'vabcl_regis', 'vbdyo_regis', 'vabxi_regis', 'vbdym_regis', 'vabxo_regis',
                   'vbdyp_regis',
                   'vabxr_regis', 'vbdyz_regis', 'vacvd_regis', 'vbdzo_regis', 'vacvj_regis', 'vbhkc_regis',
                   'vacvk_regis',
                   'vbhke_regis', 'vacvp_regis', 'vbhkf_regis', 'vacvr_regis', 'vbhkh_regis', 'vadbj_regis',
                   'vbhks_regis',
                   'vafxd_regis', 'vbhvd_regis', 'vafzh_regis', 'vbhvs_regis', 'vagab_regis', 'vbhvt_regis',
                   'vagan_regis',
                   'vbilo_regis', 'vagas_regis', 'vbjsa_regis', 'vahrb_regis', 'vbkpc_regis', 'vahrk_regis',
                   'vbkpy_regis',
                   'vahrt_regis', 'vbktr_regis', 'vaiwt_regis', 'vbnci_regis', 'vaiwx_regis', 'vbnck_regis',
                   'valor_regis',
                   'vbnvx_regis', 'vanso_regis', 'vcctk_regis', 'vanzr_regis', 'vceen_regis', 'vaobb_regis',
                   'vcfaw_regis',
                   'vaokz_regis', 'vcffg_regis', 'vaowg_regis', 'vcffm_regis', 'vapmc_regis', 'vdbwt_regis',
                   'vapmu_regis',
                   'vderc_regis', 'vaqfu_regis', 'vdgvt_regis', 'vaqyc_regis', 'vdpss_regis', 'vaqyj_regis',
                   'vdrvj_regis',
                   'vaqyv_regis', 'veamh_regis', 'vaszj_regis', 'vecyw_regis', 'vatnl_regis', 'vedtp_regis',
                   'vatno_regis',
                   'vedzt_regis', 'vatnx_regis', 'veeuc_regis', 'vauaq_regis', 'veglw_regis', 'vauid_regis',
                   'vegwm_regis',
                   'vauij_regis', 'vfcci_regis', 'vauix_regis', 'vfdnc_regis', 'vawau_regis', 'vfdnh_regis',
                   'vawhj_regis',
                   'vfetp_regis', 'vaxle_regis', 'vflex_regis', 'vaxll_regis', 'vhhap_regis', 'vaxlv_regis',
                   'vaxsk_regis',
                   'vaxsm_regis', 'vbacl_regis', 'vbdbc_regis', 'vbdzq_regis', 'vbepf_regis', 'vbfzp_regis',
                   'vbgnb_regis',
                   'vbgux_regis', 'vbgyq_regis']
    excel_name = datetime.datetime.now().strftime('%m_%d_%H_%M_%S')  # for execl name
    actual_result_list = []  # Save actual results 把返回为空用candidates1替换
    real_result_list = []  # 真实的返回结果，不管返回是否为空
    candidates1_list = []  # Save predicted results also candidates1_list
    wav_list = []  # 生成excel中wav列
    during_time = []  # 每次测试的耗时
    candidates2_list = []  
    count_null = []  # 记录返回为空的个数
    total_time_list = []
    acc_list = []
    acc_null_list = []
    k = 0
    score1_list = []
    score2_list = []

    for i in range(int(n)):
        test_wav = sample(all_list, 1)[0]  # 从测试音频中随机抽取1个
        wav_list.append(test_wav)  # excel中wav列
        candidates1 = test_wav[:5] + '_regis'  # 根据音频定位它的speakerId，定为候选人1号
        candidates1_list.append(candidates1)
        if candidates1 in register100:
            register100.remove(candidates1)
            candidates2 = sample(register100, 1)[0]  # 从另外99人中抽1人，定为候选人2号
            candidates2_list.append(candidates2)
        else:
            print("%s does not exist." % candidates1)
            return

        start_time = datetime.datetime.now()  # 测试开始
        result = os.popen('curl "http://192.168.99.214:19001/recognize_test?filename=' + remote_path + test_wav +
                          "&ranges=" + candidates1 + '|' + candidates2 + '"')  # 测试命令
        res1 = result.read()
        print(res1)
        end_time = datetime.datetime.now()  # 测试结束
        res = res1.split('|')[0]
        if res1 == 'None':  # 返回为空
            actual_result_list.append(candidates1)
            k += 1
        else:
            try:
                score1 = round(float(res1.split('|')[1]), 3)  # 得分取小数点后3位
                score2 = round(float(res1.split('|')[2]), 3)
                actual_result_list.append(res)
                score1_list.append(score1)
                score2_list.append(score2)
            except Exception as e:
                print(e)
                print(res1)
                return

        real_result_list.append(res)
        during_time.append((end_time - start_time).total_seconds())  # 每一次测试返回的时间，组成列表

        all_list = list(set(all_list).difference(set(wav_list)))  # 不放回测试，测过的就从all_list中滤过
        register100.append(candidates1)  # 把删掉的加回去
    total_time = sum(during_time)  # 耗时总长
    acc = accuracy_score(candidates1_list, actual_result_list)            # 求把返回为空当作正确时的准确率
    acc_null = accuracy_score(candidates1_list, real_result_list)  # 求把返回为空当作错误时的准确率
    acc_null_list.append(acc_null)
    total_time_list.append(total_time)
    count_null.append(k)
    acc_list.append(acc)

    for i in range(len(candidates1_list) - 1):
        count_null.append(' ')
        total_time_list.append(' ')
        acc_list.append(' ')
        acc_null_list.append(' ')

    dit = {'wav': wav_list, 'actual_name': candidates1_list, 'predicted_name': real_result_list, 
           'candidate1': candidates1_list, 'score1': score1_list, 'candidate2': candidates2_list, 'score2': score2_list,
           'time': during_time, 'null_number': count_null, 'total_time': total_time_list, 'acc1': acc_list, 
           'acc2': acc_null_list}
    file_path = r'2speakers_' + str(n) + '_' + excel_name + '.xlsx'
    writer = pd.ExcelWriter(file_path)
    df = pd.DataFrame(dit)
    df.to_excel(writer, columns=['wav', 'actual_name', 'predicted_name', 'candidate1', 'score1', 'candidate2', 'score2',
                                 'time', 'null_number', 'total_time', 'acc1', 'acc2'],
                index=False, encoding='utf-8', sheet_name='2speakers_' + wav_txt[:-4] + '_'+str(n), float_format='%.6f')
    writer.save()


if __name__ == '__main__':
    wav_txt = sys.argv[1]
    remote_path = sys.argv[2]
    times = sys.argv[3]
    if len(sys.argv) != 4:
        print("Unknown option.")
        sys.exit()
    if wav_txt[-4:] != '.txt':
        print("The first parameter is not txt.")
        sys.exit()
    if not remote_path[-1:] == '/':
        print('Please check the second parameter.')
        sys.exit()
    if not str(times).isdigit():
        print("The third parameter is not a number.")
        sys.exit()
    test2speakers(wav_txt, remote_path, times)