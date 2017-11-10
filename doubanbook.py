import requests
import sys
from termcolor import cprint
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

g_books = []
g_draw = False

def parseHTML(text):
    soup = BeautifulSoup(text, 'html.parser')
    soup_liist = soup.find_all('div', {'class': 'result'})

    for r in soup_liist:
        pic = r.div.a.img['src']
        content_el = r.find('div', {'class': 'content'})
        title = content_el.div.h3.a.string
        rate_el = content_el.div.div.find('span', {'class': 'rating_nums'})
        rate = float(rate_el.string if rate_el is not None else 0)
        rate_person = content_el.div.div.find('span', {'class': 'subject-cast'}).find_previous_sibling('span').string
        g_books.append({
            'title': title,
            'rate': rate,
            'rate_person': rate_person,
            'pic': pic
        })
        g_books.sort(key = lambda i: i['rate'])
    if g_draw:
        draw()

def draw():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig, ax = plt.subplots()
    ax.set_xlabel('评分')
    ax.set_title('豆瓣图书')

    titles = list(map(lambda i: i['title'], g_books))
    rates = list(map(lambda i: i['rate'], g_books))
    y_pos = np.arange(len(titles))

    ax.barh(y_pos, rates, align='center',
        color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(titles)

    plt.show()

def get(word):
    r = requests.get('https://www.douban.com/search?cat=1001&q=' + word)
    if r.status_code != 200:
        cprint('request failed, status code: ' + r.status_code)
    else:
        parseHTML(r.text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        cprint('missing search word', 'red')
    elif len(sys.argv) == 2:
        get(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[2] == 'd':
        g_draw = True
        get(sys.argv[1])