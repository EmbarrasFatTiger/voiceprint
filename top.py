# encoding='utf-8'

import subprocess
import time

with open('/data/voiceprint_pressure_test_records/records/test/top.txt', 'w') as f:
    for i in range(48):
        top_info = subprocess.Popen('top -b -c -d 2 -n 1 -p 30526', stdout=subprocess.PIPE, shell=True)
        out, err = top_info.communicate()
        out_info = out.decode('utf-8')
        f.write('\n'+'--------------------------------------------------'+'I am a dividing line:  '+str(i)+'------------------------------------------------'+'\n\n')
        f.write(out_info)
        print(out_info)
        time.sleep(1800)



