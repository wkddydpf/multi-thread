import json
import gzip
import pandas as pd
import numpy as np
import csv

df = pd.read_csv('argon_label_lst.csv', delimiter=',', encoding='utf-8',header=None)
print(df.head())
df.columns=['label', 'label_code']

dic = df.set_index('label').T.to_dict()
codes = df['label_code']
dic2 = {}
for c in codes:
    dic2[c] = 0

all_contents = []
for i in range(10):
    print('load', i)
    with gzip.open(f'argonjson/{i}.json', 'r') as f:
        content = f.read().decode("utf-8") 
    all_contents.append(content)

all_contents = '\n'.join(all_contents)
all_contents = all_contents.split('\n')
print('loaded, #=', len(all_contents))

img_urls=[]
nothingcnt=0
for i in range(len(all_contents)):
    print(i)
    if all_contents[i]=='':
        nothingcnt+=1
    else:
        data = json.loads(all_contents[i])
        label = data['label']
        label_code = dic[label]['label_code']
        dic2[label_code]+=1
        for s in data['samples']:
            imgurl = f"http://img1-beta.daumcdn.net/thumb/C256x256.fjpeg/?fname={s['encoded_imgurl']}"
            img_urls.append([label,label_code,imgurl])

print('Number of image urls retreieved: ',len(img_urls))
print('Number of blank classes: ', nothingcnt)

print('Checking which classes were not matched: ')
for c in codes:
    if(dic2[c]==0):
        print(c)
np.savetxt('Argon434_imgurls.csv',img_urls, delimiter='\t', fmt='%s', encoding='utf-8')