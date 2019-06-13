import re
import pysnooper


def replace_char(string, char, index):
    string = list(string)
    string[index] = char
    return ''.join(string)


# @pysnooper.snoop()
def combine_noisetype():
    key = open('E:\\Newdataset\\key - 副本.csv', 'r')
    export_new = open('E:\\Newdataset\\new000.csv', 'w')
    noise_type = open('E:\\Newdataset\\vox_noise.csv', 'r')
    key_line = key.readlines()
    noise_line = noise_type.readlines()
    for i in range(len(key_line)):
        key1 = key_line[i]
        key_split = key1.split(',')[2]
        for noise1 in noise_line:
            noise_split = noise1.strip().split(',')
            if key_split == noise_split[1][:-4]:
                s = replace_char(list(key1), noise_split[3].strip('\n'), len(list(key1)) - 3)
                print(s.strip())
                export_new.write(s)
                noise_line.remove(noise1)
                break
        else:
            print(key1.strip())
            export_new.write(key1)

    key.close()
    noise_type.close()
    export_new.close()


if __name__ == '__main__':
    combine_noisetype()