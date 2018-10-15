#!/usr/bin/env python

import math
import sys
import argparse
import subprocess
import os

args= None
RESULTS_DIC = {}
prop_keys = []

ANALYZE_COMMAND = ''


def main_f():
    init()
    dir_path = args.dir
    analyze_dir(dir_path)
    print_csv(prop_keys, RESULTS_DIC)


def analyze_dir(main_dir_path):
    results_dir = []
    for x in os.listdir(main_dir_path):
        if os.path.isdir(main_dir_path+"/"+x) and ('.' not in x):
            results_dir.append(x)

    for dir in results_dir:
        dir_arr = dir.strip().split('_')
        dir_abs = os.path.abspath(main_dir_path+"/"+dir)
        if len(dir_arr) < 2:
            continue
        for file_name in os.listdir(dir_abs):
            if os.path.isfile(dir_abs+"/"+file_name):
                file_path = os.path.abspath(dir_abs+"/"+file_name)
                arr = file_name.strip().split('-')
                if len(arr) < 3:
                    continue
                analyze_file(dir, file_name, file_path)

def analyze_file(dir, file_name, file_path):
    prop = get_prop(dir, file_name)
    global prop_keys
    prop_keys = prop.keys()
    result = run_analyze(file_path)#training result
    id = prop['id']
    if(id not in RESULTS_DIC):
        RESULTS_DIC[id] = {'prop': {}, 'test': ['NA','NA','NA'], 'train': ['NA','NA','NA']}
        RESULTS_DIC[id]['prop'] = prop
	RESULTS_DIC[id][prop['Run']] = result
    else:
        RESULTS_DIC[id]['prop'] = prop
        RESULTS_DIC[id][prop['Run']] = result


def get_prop(dir, file_name):
    arr = file_name.strip().split('-')
    dir_arr = dir.strip().split('_')
    prop = {}

    prop['Part'] = dir_arr[0]
    prop['Question'] = dir_arr[1]
    if 'q' in dir_arr[1]:
	prop['Question'] = dir_arr[1][1:]
    prop['Architecture'] = 'A:23-'+arr[0]+'-1'
    prop['#_Hidden_nodes'] = arr[0]
    prop['Learning_rate'] = arr[1]
    prop['Epoches'] = arr[2].strip().split('.')[0]
    prop['Momentum'] = 'None'
    prop['Run']= 'train'
    if len(arr)==4:
        val = arr[3][:-4]
        if val == 'test':
            prop['Run'] = 'test'
        else:
            prop['Momentum'] = arr[2]
            prop['Epoches'] = val
    elif len(arr)==5:
        prop['Run'] = 'test'
        prop['Momentum'] = arr[2]
        prop['Epoches'] = arr[3]


    prop['id'] = dir+'_'+prop['#_Hidden_nodes']+prop['Learning_rate']+prop['Epoches']
    return prop

def run_analyze(file_path):
    result = []
    num_of_pattren = '1'
    analyze = os.path.join(ANALYZE_COMMAND)
    output = subprocess.Popen([analyze, "-s", "-i", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in output.stdout:
        line = line.strip()
    	if (':' in line)  and ('%' in line):
        	data = line.split(':')
        	values = data[1].strip().split('%')
        	jData = {}
        	jData[data[0].strip()] = values[0].strip()
        	result.append(values[0].strip())
        elif (':' in line)  and ('error' in line):
            data = line.split(':')
            values = data[1].strip().split('%')
            jData = {}
            jData[data[0].strip()] = values[0].strip()
            error = values[0].strip()
            mse = "???"
            result.append(error)
            result.append(str(mse))
        elif ('STATISTICS' in line):
            data = line.split('(')
            num_of_pattren = data[1].strip().split(' ')[0]


    return result


def print_csv(prop_keys,json_obj):
    flag = True
    for key in json_obj.keys():
        if flag:
            print_labels(prop_keys, json_obj[key])
            flag = False
        ps = []
        for p in prop_keys:
            ps.append(json_obj[key]['prop'][p])
        print ','.join(ps)+','+','.join(json_obj[key]['train'])+','+','.join(json_obj[key]['test'])


def print_labels(prop_keys, record):
    length = len(record['train'])/4
    if len(record['test'])/4 > len(record['train'])/4:
        length = len(record['test'])/4
    train_labels = ''
    test_labels = ''
    for index in range(length):
        i = str(index)
        train_labels = train_labels + ',TRAIN-ERROR'+i+',train-right'+i+',train-unknown'+i+',train-tse'+i+',TRAIN-MSE'+i
        test_labels = test_labels + ',TEST-ERROR'+i+',test-right'+i+',test-unknown'+i+',test-tse'+i+',TEST-MSE'+i
    print ','.join(prop_keys) + train_labels + test_labels


def init():
    parser = argparse.ArgumentParser(description='sub-directories naming pa_b a: part number, b: question number. Files naming c-d-e-f-g.res, c: hidden-units, d: Learning_rate, e: Momentum (optional), f: cycles, g: "test" (optional). For example: 10-0.2-1000.res, 10-0.2-0.5-1000.res, 10-0.2-1000-test.res, 10-0.2-0.5-1000.res')
    required_arguments = parser.add_argument_group('Required arguments')
    required_arguments.add_argument("-d", "--dir",  help="Results directory which containes all sub-direcotries which containe .res files", required=True)


    global args
    args = parser.parse_args()



#run the programe
main_f()
