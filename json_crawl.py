import json
import glob

# 찾으려는 attributes
target = ['구급차', '소방차', '경찰차']
# 메인 파일 directory
dir_path = "RoadData\\**\\**\\**\\**\\*.json"
print(dir_path)
res = []

loc_with_emergency = []

# dir_path내 모든 파일 경로 찾기
for file in glob.glob(dir_path, recursive=True):
    # print(file)
    res.append(file)
    
print(len(res))

# 파일 열어보면서 응급차들 찾기
for line in res:
    cur = line.split('\\')[2]
    if cur not in loc_with_emergency:
        try:
            with open(line, 'rt', encoding='UTF8') as f:
                data = json.load(f)    
        except:
            print("source error: ")
            print(line)
            continue

        for r in data['row']:
            if r['attributes2'] in target:
                print(line.split('\\')[2])
                print(r['attributes2'])
                loc_with_emergency.append(line.split('\\')[2])
                break
        f.close()
print(loc_with_emergency)

'''
결과
['야간_과천_01', 
 '야간_성남_01', 
 '야간_성남_02', 
 '야간_성남_03', 
 '야간_성남_04', 
 '야간_수원_01', 
 '야간_수원_02', 
 '야간_안산_01', 
 '야간_안산_02', 
 '야간_안산_03', 
 '야간_안양_01', 
 '야간_안양_02', 
 '야간_안양_03', 
 '야간_안양_04', 
 '야간_오산_01', 
 '야간_용인_01', 
 '야간_용인_02', 
 ' 야간_용인_03', 
 '야간_의왕_01', 
 '야간_화성_01', 
 '야간_화성_02', 
 '주간_성남_01', 
 '주간_성남_04', 
 '주간_성남_05', 
 '주간_성남_06', 
 '주간_성남_07', 
 '주간_성남_08', 
 '주간_수원_01', 
 '주간_수원_02', 
 '주간_수원_03', 
 '주간_수원_04', 
 '주간_안산_01', 
 '주간_안양_01', 
 '주간_안양_02', 
 '주간_용인_01', 
 '주간_용인_02', 
 '주간_의왕_01', 
 '주간_의왕_02']
 '''