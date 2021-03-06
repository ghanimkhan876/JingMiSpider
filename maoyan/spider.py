import json
import re
from multiprocessing.pool import Pool

import requests
from requests.exceptions import RequestException


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    print(items)
    print(type(items))
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:#'a'追加字符串模式写入
        f.write(json.dumps(content,ensure_ascii=False)+'\n')#json.dumps把字典转换成字符串
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    #print(html)
    parse_one_page(html)
    for item in parse_one_page(html):
         print(item)
         write_to_file(item)


if __name__ == '__main__':
    pool = Pool()#进程池,提供指定进程给用户调用,如果池未满且有新的请求就开启多个进程,满了就等待
    pool.map(main,[i*10 for i in range(10)])#pool.map把数组中的每一个元素当做函数的参数

