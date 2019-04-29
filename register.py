# -*- coding: utf-8 -*
import os
import sys


def register(wav_list, remote_path):
    """
    :param wav_list: 包含远程音频文件名的txt
    :param remote_path: 远程音频所在文件夹的路径
    :return:
    """
    with open(wav_list, 'r') as f:  # 打开注册文件名列表
        for line in f.readlines():
            name = line.strip('\n')
            os.system('curl "http://192.168.99.214:19001/register?filename=' + remote_path + name + '"')  # 注册命令
            # print('curl "http://192.168.99.214:19001/register?filename=' + remote_path + name + '"')


if __name__ == '__main__':
    wav_list = sys.argv[1]
    remote_path = sys.argv[2]

    if len(sys.argv) != 3:
        print("Unknown option.")
        sys.exit()

    register(wav_list, remote_path)