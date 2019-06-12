# coding=UTF-8
import time
from flask import Flask, request
from functools import reduce
# from feature_compute import Get_Evaluate_Enrollment_Feature
# from feature_compute import return_results, return_only_results, FeatureMapping
from feature_compute import FeatureMapping
import json

app = Flask(__name__)
res = {}  #    ?  ?
res_score = []
res_vertify = {}  #    ?  ?
maxlen_per_user = 5  # ??   ?   ? ÷?  ??     10  ?    10 ?/30
register_data_path = '/data/register'

Enrollment_png_path = '/data/Enrollment_png'
Enrollment_Feature_path = '/data/Enrollment_Feature'

evaluate_data_path = '/data/validation'
Evaluation_saved_png_path ='/data/Evaluate_png'

swindle_data_path = '/data/swindle'
Swindle_saved_png_path ='/data/Swindle_png'
Swindle_feature_path='/data/Swindle_Feature'

feature_mapping = FeatureMapping()
#    ÷  ??
@app.route('/register', methods=['GET'])
def register():
    start_time = time.time()  # seconds
    filename = request.values.get("filename")  # ?   ?  ж ?key  value?
    print('filename:', filename)

    the_label = str(filename).split('/')[-1].split('.')[0]
    print('request the_label:', the_label)

    signal = feature_mapping.Get_Evaluate_Enrollment_Feature(None, the_label, Enrollment_png_path, Enrollment_Feature_path, filename)
    end_time = time.time()
    print('eating time is :', end_time - start_time)
    # print('signal:', signal)
    if signal is not None:
        return 'true'
    print('We can not squeeze voice feature for the bad voice by NXG......')
    return 'false'


# ? ?   ?  ?        phonenum        ?? null
@app.route('/recognize', methods=['GET'])
def recognize():
    # ?   ?  ж ?key  value?
    start_time = time.time()
    filename = request.values.get("filename")
    print('file name:', filename )
    # get current enrollment user
    sperker_id = request.values.get("ranges")
    print('sperker_id name:', sperker_id)
    all_users = sperker_id.strip().split('|')  # get all use id
    print('all_users:', all_users)
    assert len(all_users) > 0, 'must submit user id'
    the_label = str(filename).split('/')[-1].split('.')[0]
    evaluation_feature = feature_mapping.Get_Evaluate_Enrollment_Feature(None, the_label, Evaluation_saved_png_path, None, filename)
    end_time = time.time()
    print('eating time is :', end_time - start_time)
    if evaluation_feature is not None:
        # ?     ?  ?
        number, max_score = feature_mapping.return_results(Enrollment_Feature_path, evaluation_feature, all_users)
        #       ??   ?    ?    ? ?     ?          ? ?     ?  ?    ? δ? ?
        if max_score >= 0.5:
            if number not in res.keys():
                res[number] = [max_score]  #      ? ?  ?   ?
            else:
                if len(res[number]) >= maxlen_per_user:  #  ?   ?    ?   ?
                    res[number] = []
                    res[number].append(max_score)
                else:
                    res[number].append(max_score)
            #          ?    ?   ?  ?            ? ?    ?
            print('score list is:', res)
            if max_score >= 0.5:
                print(' max_score above thread:',  (max_score, number))
                res_score.append(number)
                # print('score saved:', res_score)
                print('number:', number)
                print('#' * 100)
                return number
            avg_score = reduce(lambda cur_score_pre, cur_score: cur_score_pre + cur_score, res[number]) / len(res[number])
            print('avg score is:', avg_score)
            if avg_score >= 0.5:
                print('number:', number)
                res_score.append(number)
                # print('score saved:', res_score)
                print('#' * 100)
                return number
            else:
                return ''  #           ?    ?   ?
        else:
            return ''  #         ?      ?
    else:
        return ''  #       ??



@app.route('/verify', methods=['GET'])
def verify():
    # ?   ?  ж ?key  value?
    start_time = time.time()
    filename = request.values.get("filename")
    the_label = str(filename).split('/')[-1].split('.')[0]  # id_time
    _the_label = str(the_label).split('_')[0]  # id
    print('vertify label:', the_label)
    # signal = feature_mapping.Get_Evaluate_Enrollment_Feature(the_label, _the_label, Evaluation_saved_png_path, None, filename, is_register=False)
    signal = feature_mapping.Get_Evaluate_Enrollment_Feature(None, _the_label, Evaluation_saved_png_path, None,
                                                             filename)
    if signal is not None:
        # return_only_results(self, Saved_Feature_path, Evaluated_Feature, the_label)
        # 一对一任然要返回手机号码和得分
        finding, max_score = feature_mapping.return_only_results(Enrollment_Feature_path, signal, _the_label)
        if finding:  # 找到了这个人
            if the_label not in res_vertify.keys():
                # if res_vertify.get(number, 'not_in_mind') == 'not_in_mind':
                res_vertify[the_label] = [max_score]
            else:
                if len(res_vertify[the_label]) == maxlen_per_user:  #  ?   ?    ?   ?
                    res_vertify[the_label] = []
                    res_vertify[the_label].append(max_score)
            #          ?    ?   ?  ?            ? ?    ?
            print('score list:', res_vertify)
            if len(res_vertify[the_label]) == 1:
                avg_score = res_vertify[the_label][0]
            else:
                avg_score = reduce(lambda cur_score_pre, cur_score: cur_score_pre + cur_score,
                                   res_vertify[the_label]) / len(res_vertify[number])
            print('avg_score:', avg_score)
            end_time = time.time()
            print('eating time is :', end_time - start_time)
            if avg_score > 0.71:
                return 'true'
            else:
                return 'false'
        else:
            return 'false'
    else:
        return 'false'

'''
swindle_data_path = '/data/swindle'          WAV
Swindle_saved_png_path ='/data/Swindle_png'   PNG
Swindle_feature_path='/data/Swindle_Feature'    NPY
'''

# ???          true or false
@app.route('/swindle', methods=['GET'])
def swindle():
    # ?   ?  ж ?key  value?
    filename = request.values.get("filename")
    # score = return_results(registered_Featuer_path, evaluate_data)
    # print('score:', score)
    # return score

    the_label = str(filename).split('/')[-1].split('.')[0]
    print('request the_label:', the_label)
    signal = feature_mapping.Get_Evaluate_Enrollment_Feature(None,the_label,Swindle_saved_png_path,None,filename)
    # print('signal:', signal)
    if signal is not None:
        #     ÷
        # label,score=return_results(Enrollment_Feature_path,signal)
        result = feature_mapping.return_results(Enrollment_Feature_path, signal)
        print('result:', result)
        if result:
            return 'true'
    return 'false'


#     ? ÷
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19001)  # 19001