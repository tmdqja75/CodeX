import json, glob, os
from tqdm import tqdm
import pathlib

# 문제 1: 절대경로를 가져와서 적용하는 법  /   pathlib를 활용해 해결
# 문제 2: r['attributes2'] 를 한번씩 탐색 할때마다 경로를 가져와서 결국에는 모든 경로가 가져와짐, 중복도 됨, / cnt를 추가해 해결

def search(target):
    # 찾으려는 attributes
    # 메인 파일 directory
    # .\\1.Training\\원천데이터\\주간\\주간_성남_01\\성남_주간_2021-08-30-17-38-59\\Front_View_CMR\\2021-08-30-17-38-59_Front_1630312754200.png

    # dir_path = "./1.Training/**/주간/**/**/**/*.json"  # 경로 수정.
    # dir_path = ".\\1.Training\\**\\주간\\**\\**\\**\\*.json"
    dir_path = ".\\1.Training\\라벨링데이터\\주간\\주간_성남_01\\**\\**\\*.json"  # 경로 수정
    print(dir_path)
    res = []
    del_list = []  # 추가
    json_list = []
    cnt = 0

    # dir_path내 모든 파일 경로 찾기
    for file in glob.glob(dir_path, recursive=True):
        # print(file)
        res.append(file)

    print(len(res))

    # 파일 열어보면서 응급차가 없는 json 파일 찾기
    for line in tqdm(res):
        cnt = 0
        try:
            with open(line, 'rt', encoding='UTF8') as f:
                data = json.load(f)
        except:
            print("source error: ")
            print(line)
            continue

        for r in data['row']:        # 한개의 json을 스크래핑을 하며 target이 있는지 갯수를 구함
            if r['attributes2'] in target :
                cnt += 1

        if cnt > 0:                  # 한개라도 존재 하면 살리는 json
            json_list.append(list)
        else:                        # 존재하지 않으면 없애는 json 및 file
            p = line.split('\\')
            k = p[-1].split('.')
            path = "\\" + p[1] + "\\원천데이터\\" + "\\".join(p[3:7]) + "\\" + ".".join(k[:2])
            del_list.append(line[1:])
            del_list.append(path)

        f.close()

    print(f"총 : {len(json_list)} 개 살림림.")
    print(f"총 : {len(del_list)} 개 삭제.")
    return del_list, json_list, res


# json + jpg 같이삭제
def delete(file_path):
    root = str(pathlib.Path.cwd())
    for path in tqdm(file_path):
        if os.path.exists(root+path):
            r = root + path
            os.remove(r)
            print("삭제")
        else:
            print("파일 존재 안 함")


def change_txt(file_path, target):
    lis = []
    di = {v: i for i, v in enumerate(target)}
    for line in tqdm(file_path):
        try:
            with open(line, 'rt', encoding='UTF8') as f:
                data = json.load(f)
        except:
            print("source error: ")
            print(line)
            continue
        for r in data['row']:
            if r['attributes2'] in target:
                name = di[r["attributes2"]]

                w = r["width"]
                h = r["height"]
                x1 = int(r["points1"].split(",")[0])
                y1 = int(r["points1"].split(",")[1])
                x2 = int(r["points3"].split(",")[0]) - int(r["points1"].split(",")[0])
                y2 = int(r["points3"].split(",")[1]) - int(r["points2"].split(",")[1])

                dw = 1. / w
                dh = 1. / h
                x = (float(x1) + float(x1) + float(x2)) / 2.0
                y = (float(y1) + float(y1) + float(y2)) / 2.0
                w = float(x2)
                h = float(y2)

                x = round(x * dw, 6)
                w = round(w * dw, 6)
                y = round(y * dh, 6)
                h = round(h * dh, 6)

                lis.append(name + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + "\n")
    return lis


target = ['구급차', '소방차', '경찰차']
del_list, json_list, res = search(target)
print(len(del_list), len(json_list), len(res))
delete(del_list)