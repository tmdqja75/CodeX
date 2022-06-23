import glob
import os
import json
import shutil

from tqdm import tqdm

def box_convert(x1, x2, y1, y2, w, h):
    x_c = str(((x2+x1)/2)/w)
    y_c = str(((y2+y1)/2)/h)
    width = str((x2-x1)/w)
    height = str((y2-y1)/h)
    return x_c+' '+y_c+' '+width+' '+height
    

def json_to_txt(json_file, txtpath, img_dest):
    target = ['구급차', '소방차', '경찰차']
    result_line = ''
    try:
        with open(json_file, 'rt', encoding='UTF-8') as f:
            data = json.load(f)
    except:
        print('Source Error!')
        print(json_file)
        return
    if len(data['row'])==0:
        return
    
    height = data['row'][0]['height']
    width = data['row'][0]['width']
    
    path_split = json_file.split('/')
    txt_path_end = path_split[-1][:-8]+'txt'

    txtpath = txtpath+txt_path_end
    
    is_emergency = False
    for r in data['row']:
        if r['attributes2'] in target:
            is_emergency = True
            p1 = [int(i) for i in r['points1'].split(',')]
            p3 = [int(i) for i in r['points3'].split(',')]
            b = box_convert(p1[0], p3[0], p1[1], p3[1], width, height)
            class_num = str(target.index(r['attributes2']))
            result_line += class_num+' '+b+'\n'
    
    if is_emergency:
        path_split[3] = "원천데이터"
        img_path_end = '/'+path_split[-1][:-8]+'jpg'
        final_path = '/'.join(path_split[:-1])+img_path_end
        # print(final_path)
        shutil.copy(final_path, img_dest)        
    if result_line:
        # print(result_line)
        # print("text file path: ", txtpath)
        file_out = open(txtpath, "w")
        file_out.write(result_line)
        file_out.close()
    
    f.close()
    
# json파일이 모여있느 파일 디렉토리
json_dir_path = './교통CCTV인공지능학습용데이터_Train/1.Training/라벨링데이터/**/**/**/*.json'
# txt파일으 저장하 파일 디렉토리
txtpath = './labels/'
# 응급차가 담겨있느 이미지르 따로 저장할 파이 디럭토리
img_dest = './images/'

for file in tqdm(glob.glob(json_dir_path, recursive=True), desc="Emergency Vehicle txt file extraction"):
    json_to_txt(file, txtpath, img_dest)
