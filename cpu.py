# encoding='utf-8'
import re
import pandas as pd

PID_list = []
USER_list = []
PR_list = []
NI_list = []
VIRT_list = []
RES_LIST = []
SHR_LIST = []
S_list = []
CPU_list = []
MEM_list = []
TIME_list = []
COMMAND_list = []

with open('4-39600-400-top.txt', 'r') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if re.findall('30526', lines[i]):
            PID_list.append(lines[i].split()[0])
            USER_list.append(lines[i].split()[1])
            PR_list.append(lines[i].split()[2])
            NI_list.append(lines[i].split()[3])
            VIRT_list.append(lines[i].split()[4])
            RES_LIST.append(lines[i].split()[5])
            SHR_LIST.append(lines[i].split()[6])
            S_list.append(lines[i].split()[7])
            CPU_list.append(lines[i].split()[8])
            MEM_list.append(lines[i].split()[9])
            TIME_list.append(lines[i].split()[10])
            COMMAND_list.append(lines[i].split()[11])


dit = {'PID': PID_list, 'USER': USER_list, 'PR': PR_list, 'NI': NI_list, 'VIRT': VIRT_list, 'RES': RES_LIST, 'SHR':SHR_LIST,
       'S': S_list, '%CPU': CPU_list, '%MEM': MEM_list, 'TIME+': TIME_list, 'COMMAND': COMMAND_list}
file_path = r'C:/Users/杨杰/Desktop/声纹识别/第二次测试/' + 'top' + '.xlsx'
writer = pd.ExcelWriter(file_path)
df = pd.DataFrame(dit)
df.to_excel(writer, columns=['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND'],
            index=False, encoding='utf-8', float_format='%.1f')
writer.save()