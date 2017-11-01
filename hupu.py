
from collections import deque
from urllib import request
import re

queue = deque()
urlSet = set()
pro = dict()


def pageurl(url):
    req = request.urlopen(url)
    html = req.read().decode('GBK', errors='ignore')
    reg = r'http://my.hupu.com/\d{7}'
    urlre = re.compile(reg)
    urllist = re.findall(urlre, html)
    return urllist


def store(url):
    req = request.urlopen(url)
    html = req.read().decode('GBK', errors='ignore')
    reg = r'<span itemprop="address">[\u4e00-\u9fa5]+</span>'
    provinre = re.compile(reg)
    provinlist = re.findall(provinre, html)
    for province in provinlist:
        if province[25:27] in pro:
            pro[province[25:27]] += 1
        else:
            pro[province[25:27]] = 1

# 111111111 可以换成自己的虎扑号			
startPoint = "http://my.hupu.com/111111111" 
queue.append(startPoint)
urlSet.add(startPoint)
while len(queue) > 0 and len(urlSet) < 50000:
    top = queue.popleft()
    try:
        for point in pageurl(top):
            if point not in urlSet:
                store(point)
                queue.append(point)
                urlSet.add(point)
    except Exception as e:
        continue

for k in pro:
    f = open('f:\\result.txt', 'a')
    f.write(k + ' ' + str(pro[k]) + '\n')
    f.close()

