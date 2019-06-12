import shutil
import os


path = 'E:\\Newdataset\\3vox\\'
s_id = os.listdir(path)
with open('E:\\Newdataset\\new 1.csv', 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
        id = line.strip().split(',')[1]
        sex = line.strip().split(',')[2]
        print(id, sex)
        if sex == 'male':
            try:
                shutil.copytree(os.path.join(path, id), os.path.join('G:\\DATASET\\VOX\\male\\', id))
            except Exception as e:
                print(e)
                continue
        elif sex == 'female':
            try:
                shutil.copytree(os.path.join(path, id), os.path.join('G:\\DATASET\\VOX\\female\\', id))
            except Exception as e:
                print(e)
                continue

