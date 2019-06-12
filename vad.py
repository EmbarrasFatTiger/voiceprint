__author__ = 'NXG'
import sys
import os, wave
import webrtcvad
import contextlib
import collections
from math import ceil, floor
from copy import deepcopy

saved_original_voice_path = '/data/validation_clip/'


def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        """
        wave file basic info:
            _wave_params:
                nchannels=1,
                sampwidth=2,
                framerate=8000,
                nframes=1088000,
                comptype='NONE',
                compname='not compressed'

        """
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000)  #
        pcm_data = wf.readframes(wf.getnframes())  # nframs is: 1088000  read all data one time
        # note: len of pcm_data is 2176000
        print('the voice length is:{} and sample_rate is:{}'.format(len(pcm_data), sample_rate))
        return pcm_data, sample_rate  # return row data & sample rate


def write_wave(path, audio, sample_rate):
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(audio)
    wf.close()


class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_collect(frame_duration_ms, audio, sample_rate):
    # audio: all the data
    frame_segment = []
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)  # 30ms   30ms / 1000ms  2 <-> s bytes
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0  # sub second
    while offset + n < len(audio):  # if 1s n = 8000*2
        """
            0-8000*2  0.0  1
            8000*2- 8000*2+8000 1, 1
            8000*2+8000- 8000*2+8000+8000 2 1
        """
        frame_segment.append(Frame(audio[offset:offset + n], timestamp, duration))
        timestamp += duration
        offset += n
    # print('collect all frams:', len(frame_segment))
    return frame_segment  # 4533


def vad_check(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames, write_path, saved_original_voice=False):
    less_than_3_s = False
    num_padding_frames = int(padding_duration_ms // frame_duration_ms)  # 3000 /30   100 frame
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    for index_, frame in enumerate(frames):
        ring_buffer.append(frame)
    # human_voiced = ring_buffer
    human_voiced = [f for f in ring_buffer if vad.is_speech(f.bytes, sample_rate)]  # gather human voice55555
    ring_buffer_human = collections.deque(maxlen=num_padding_frames)
    for human_voices in human_voiced:
        ring_buffer_human.append(human_voices)
    human_voiced = b''.join([seg.bytes for seg in ring_buffer_human])
    #  the voice channel is 2, so length of 0.5 second voice is 16000 *1=16000
    human_voiced_len = len(human_voiced)
    if human_voiced_len < 16000 * 2:  # human voice length less than 1s
        print('bad human voice length:',  human_voiced_len / (16000 * 2))
        ring_buffer.clear()
        return []  # not human voice
    else:
        if saved_original_voice:  # save the original voice
            write_path_original = saved_original_voice_path.__add__(write_path.strip().split('/')[-1])
            ring_buffer = b''.join([seg.bytes for seg in ring_buffer])
            write_wave(write_path_original, ring_buffer, sample_rate)  # original voice

        if human_voiced_len < 16000 * 5:  # human voice length in [0.5s, 1s]  #  Modify here
            # human_voiced = human_voiced.__add__(human_voiced)  # Modify here  96000 /  11520 = 8
            full_human_voice_length = 16000 * 6
            copy_num = ceil(full_human_voice_length / human_voiced_len)
            tmp = deepcopy(human_voiced)
            for copy_step in range(1, copy_num, 1):   # 3s   1.1s
                human_voiced = human_voiced.__add__(tmp)  # Modify here
            less_than_3_s = True
        write_wave(write_path, human_voiced, sample_rate)
        return [less_than_3_s, human_voiced, sample_rate]


def check(*path):

    audio, sample_rate = read_wave(path[1])  # read the wav format voice data
    print('voice sample_rate:',  (sample_rate, len(audio)))
    vad = webrtcvad.Vad(int(path[0]))  # vad detection
    frames = frame_collect(30, audio, sample_rate)
    frames = list(frames)
    return vad_check(sample_rate, 30, len(frames) * 30, vad, frames, path[1])


if __name__ == '__main__':
    path = 'E:\\Newdataset\\1nist\\'
    saved_path = 'D:\\webrtcvad_nist\\'
    all_data_set_path = list(map(lambda x: os.path.join(path, x), os.listdir(path)))  # all data set
    all_saved_data_path = list(map(lambda x: os.path.join(saved_path, x), os.listdir(path)))  # all data set
    for cur_data_set, saved_data_path, in zip(all_data_set_path, all_saved_data_path):
        # all data set data(voice)
        all_voice = list(map(lambda x: os.path.join(cur_data_set, x), os.listdir(cur_data_set)))
        all_voice_saved_path = list(map(lambda x: os.path.join(saved_data_path, x), os.listdir(cur_data_set)))
        for cur_path, cur_save in zip(all_voice, all_voice_saved_path):
            res = check(3,  cur_path)
            if len(res) > 0:
                flag, voiced, sample_rate = res[:]
                if flag:  # less than 3s
                    # demo/NIST/ss.wav
                    flag_sec = 'lower_than_3s'
                else:
                    flag_sec = 'upper_than_3s'
                if '\\' in cur_path:
                    cur_path = cur_path.replace('\\', '/')
                ss = cur_path.split('/')
                ss.insert(2, flag_sec)
                saved_p = '/'.join(ss[:])
                saved_p= saved_p.replace(ss[0], saved_path)
                saved_parent = '/'.join(saved_p.split('/')[:-1])
                print('*' * 100)
                print('saved_parent:', saved_parent)
                print('saved_p:', saved_p)
                print('*' * 100)
                if not os.path.exists(saved_parent):
                    print('saved_parent:', saved_parent)
                    os.makedirs(saved_parent)
                write_wave(saved_p, voiced, sample_rate)