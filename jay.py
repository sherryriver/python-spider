#encoding=utf8
__author__ = 'lingo'

import urllib2
import re
from bs4 import BeautifulSoup
queue = list()
page=1

#总共只有5页
while page<6:

    #帖子路径（直接看楼主）
    url= "http://tieba.baidu.com/p/3542842663?see_lz=1&pn="+str(page)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read())
    code_div = soup.find_all(class_="d_post_content j_d_post_content  clearfix")
    for code in code_div:
        #print code.prettify()

        #获取jpg图片
        code_img =  code.find_all("img",src=re.compile("jpg"))
        #print code_img
        for image in code_img:
            print "第"+str(page)+"页图片链接：",image["src"]

            #queue.append(image["src"])
    page = page + 1
else:
    print("完成")
    #写入记事本里
    #with open('image.txt','w') as f:
        #f.write(str(queue)+ '\n')






