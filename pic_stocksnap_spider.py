# coding: utf-8

from pic_getIndexHtml import page_spider
from pic_mysql_help import MysqlHelp
import threading
import time
import random
import json
import Queue

queue = Queue.Queue(maxsize=20)
tags_list = []

def sto_page():
    # 默认有下一页
    sto_nextPage = True
    # 初始化页码
    page_num = 0
    # 判断是否还有下一页
    while sto_nextPage:
        time.sleep(random.randint(1,3))
        if not queue.full():
            try:
                # 加一页
                page_num += 1
                print("=加载第" + str(page_num) + "页=")
                # 拼组分页url
                url = "https://stocksnap.io/api/load-photos/date/desc/" + str(page_num)
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
                queue.put(sto_result_lists)
                print("-第" + str(page_num) + "页加载结束-")
            except:
                print(str(page_num) + "加载出错")
                page_num -= 1
        else:
            # 如果队列满了就睡眠3s
            time.sleep(1)

def save_result_mysql():
    # global queue
    sto_nextPage = True
    page_num = 0
    mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    tag_mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    while sto_nextPage:
        while not queue.empty():
            try:
                page_num += 1
                print("<储存第" + str(page_num) + "页>")
                sto_result_lists = queue.get()
                sto_nextPage = sto_result_lists[-1]['nextPage']
                for result in sto_result_lists[:-1]:

                    # # 标签处理
                    # sto_tags_lists = result['tags'].split(",")
                    # global tags_list
                    # tag_change = False
                    # tags = ""
                    # for tag in sto_tags_lists:
                    #     if tag not in tags_list:
                    #         tag_change = True
                    #         tags_list.append(tag.strip())
                    #     tags += tag.strip() + ","
                    # print tags
                    # if tag_change:
                    #     tag_url = "alter table pic_stocksnap modify tags set(%s" + ",%s" * (len(tags_list)-1) + ")"
                    #     tag_mysql.all(tag_url,params=tags_list)

                    # 存入数据
                    url = "insert ignore into pic_stocksnap(img_id, tags_all,page_views,downloads,favorites,img_width,img_height) values(%s,%s,%s,%s,%s,%s,%s)"
                    params = [result['img_id'],result["tags"],result['page_views'],result['downloads'],result['favorites'],result['img_width'],result['img_height']]
                    mysql.cud(url,params=params)

                print("<第" + str(page_num) + "页储存成功>")
                print "-"*5 + str(tags_list) + "-"*5
            except:
                print(str(page_num) + "储存失败")
                page_num -= 1
        else:
            time.sleep(10)

def main():
    sto_page_thread = threading.Thread(target=sto_page)
    sto_result_thread = threading.Thread(target=save_result_mysql)

    sto_page_thread.start()
    time.sleep(10)
    sto_result_thread.start()

if __name__ == "__main__":
    main()



