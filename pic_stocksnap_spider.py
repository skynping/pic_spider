# coding: utf-8

from pic_getIndexHtml import page_spider
from pic_mysql_help import MysqlHelp
import threading
import time
import random
import json
import Queue
import warnings
import io

# 忽略warning
warnings.filterwarnings("ignore")
sorts_queue = Queue.Queue(maxsize=2)
queue = Queue.Queue(maxsize=20)

def sort():
    sort_list = []
    f = io.open("pic_stocksnap_sorts.txt", "r")
    for sort in f.readlines():
        sort_list.append(sort.replace("\n","").strip().lower())
    return sort_list

def sto_page():
    sorts = sorts_queue.get()
    # 默认有下一页
    sto_nextPage = True
    # 初始化页码
    page_num = 0
    # 判断是否还有下一页
    while sto_nextPage:
        time.sleep(random.randint(0,2))
        if not queue.full():
            try:
                # 加一页
                page_num += 1
                print(str(threading.currentThread().ident) + ": " + sorts + " =loading " + str(page_num) + " page=")
                # 拼组分页url
                url = 'https://stocksnap.io/api/search-photos/' + sorts + '/relevance/desc/' + str(page_num)
                # 发送get请求获取分页数据
                sto_page_spider = page_spider(url=url)
                sto_page_html = sto_page_spider.get()
                # 将字符串转为json格式
                sto_page_json = json.loads(sto_page_html['text'])
                # 判断是否还有下一页
                sto_nextPage = sto_page_json['nextPage']
                sto_result_lists = sto_page_json['results']
                # 是否有下一页存在最后一个
                sto_result_lists.append({'nextPage':sto_nextPage})
                sto_result_lists.append({'sorts':sorts})
                queue.put(sto_result_lists)
                print(str(threading.currentThread().ident) + ": " + sorts + "-loading " + str(page_num) + " over-")
            except:
                print(str(threading.currentThread().ident) + ": " + str(page_num) + "loding error in page 59")
                page_num -= 1
        else:
            # 如果队列满了就睡眠3s
            time.sleep(1)
    print(str(threading.currentThread().ident) + ":  over--------------------------------------------->")

def save_result_mysql():
    num = 0
    page_num = 0
    mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    while True:
        if not queue.empty():
            try:
                page_num += 1
                print(str(threading.currentThread().ident) + ": <saving " + str(page_num) + " >")
                sto_result_lists = queue.get()
                for result in sto_result_lists[:-2]:
                    # 存入数据
                    url = "insert ignore into pic_stocksnap(img_id, tags_all,page_views,downloads,favorites,img_width,img_height,sorts) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    params = [result['img_id'],result["tags"],result['page_views'],result['downloads'],result['favorites'],result['img_width'],result['img_height'],sto_result_lists[-1]['sorts']]
                    mysql.cud(url,params=params)
                print(str(threading.currentThread().ident) + ": <The" + str(page_num) + "saved successfully>")
            except:
                print(str(page_num) + "saving error on page 82")
                page_num -= 1

        else:
            time.sleep(2)
            num += 1
            if num > 1000:
                print(str(threading.currentThread().ident) + ": saving over-------->")
                exit()
                break

def main():

    # 按分类爬取
    sort_lists = sort()

    print("start saving!!!")
    for i in range(6):
        save_Thread_1 = threading.Thread(target=save_result_mysql)
        save_Thread_1.start()
        time.sleep(0.2)

    for sorts in sort_lists:
        # print color
        sorts_queue.put(sorts)
        color_Thread = threading.Thread(target=sto_page)
        time.sleep(0.2)
        color_Thread.start()

    print("The main thread here!!!")

if __name__ == "__main__":
    main()



