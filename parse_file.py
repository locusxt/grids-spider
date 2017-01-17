#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

question_num = 0

def read_from_file(fname):
    global question_num
    f = open(fname, 'r')
    res_list = []
    res_map = {}
    for l in f:
        tmp_list = l.split()
        uid = tmp_list[0]
        # score_list = tmp_list[1:]
        res_list.append(tmp_list)
        res_map[uid] = 0.0
    q_num = len(res_list[0]) - 1
    question_num += q_num
    for i in range(q_num):
        # print("========" + str(i + 1) + "==========")
        res_list.sort(key=lambda obj:obj[i + 1])
        # for j in res_list:
            # print (j)
        first_i = 0 
        last_i = 0
        for j in range(len(res_list) - 1, 0, -1):
            if res_list[j][i + 1] != "notpassed":
                last_i = j
                break
        num = last_i - first_i + 1
        step = 25.0 / num #根据实际情况修改
        cur = 100.0
        for j in range(first_i, last_i + 1):
            res_map[res_list[j][0]] += cur
            cur -= step
    return res_map
    # t_list = []
    # for k in res_map:
    #     t_list.append((k, res_map[k]))
    #     t_list.sort(key=lambda obj:obj[1])
    #     # print (str(k) + " " + str(res_map[k]))
    # for i in t_list:
    #     print(i)
    
if __name__ == '__main__':
    # file_name = "2.txt"
    # read_from_file(file_name)
    res_map = {}
    res_list = []
    f = open("res.csv", 'w')
    for i in range(2, 6): #读取2.txt至5.txt，此处按实际情况修改
        file_str = str(i) + ".txt"
        score_map = read_from_file(file_str)
        for (k, v) in score_map.items():
            if k not in res_map:
                res_map[k] = 0.0
            res_map[k] += v
    for (k, v) in res_map.items():
        res_list.append((k, v / question_num))
    res_list.sort(key = lambda obj:obj[1])
    for r in res_list:
        print(str(r[0]) + "," + str(r[1]), file = f)
        print(str(r[0]) + "," + str(r[1]))
    print (question_num)