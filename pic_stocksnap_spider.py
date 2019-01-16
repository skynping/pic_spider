# coding: utf-8

from pic_getIndexHtml import page_spider
from pic_mysql_help import MysqlHelp
from lxml import etree
import threading
import time
import random
import json
import Queue

queue = Queue.Queue(maxsize=20)
csrf_queue = Queue.Queue(maxsize=100)

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
    while sto_nextPage:
        while not queue.empty():
            try:
                page_num += 1
                print("<储存第" + str(page_num) + "页>")
                sto_result_lists = queue.get()
                sto_nextPage = sto_result_lists[-1]['nextPage']
                for result in sto_result_lists[:-1]:
                    # 存入数据
                    url = "insert ignore into pic_stocksnap(img_id, tags_all,page_views,downloads,favorites,img_width,img_height) values(%s,%s,%s,%s,%s,%s,%s)"
                    params = [result['img_id'],result["tags"],result['page_views'],result['downloads'],result['favorites'],result['img_width'],result['img_height']]
                    mysql.cud(url,params=params)
                print("<第" + str(page_num) + "页储存成功>")
            except:
                print(str(page_num) + "储存失败")
                page_num -= 1
        else:
            time.sleep(10)

def sto_load():
    mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    # search_url = "select img_id from pic_stocksnap where downloads > 10"
    search_url = "select img_id from pic_stocksnap"
    download_ids = mysql.all(search_url)
    load_num = 0
    for id in download_ids:
        if not queue.full():
            try:
                load_num += 1
                print("加载 <" + str(load_num) + ">")
                # load_url = "https://stocksnap.io/photo/" + str(id).replace("(","").replace(")","").replace("u","").replace(",","").replace("'","")
                load_url = "https://stocksnap.io/photo/" + str(id[0])
                load_spider = page_spider(url=load_url)

                load_text =  load_spider.get()['text']
                # 转换成xpath格式
                load_html = etree.HTML(load_text)
                # 筛选
                csrf = load_html.xpath("//div[@class='equal-columns']//form/input[1]/@value")[0]
                # 存入队列
                csrf_queue.put({"load_id":str(id[0]),"csrf":csrf,"load_num":str(load_num)})
                print("<" + str(load_num) + ">加载结束")
            except:
                print("photoid加载异常")
        else:
            time.sleep(2)

def save_csrf_mysql():
    # 初始化第二次是否为空
    is_second = False
    mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    while True:
        if not csrf_queue.empty():
            try:
                is_second = False
                photo_dict = csrf_queue.get()

                print("*" + "存 "+ photo_dict['load_num'])
                csrf_url = "insert ignore into sto_csrf(csrf,img_id) values(%s,%s)"
                params = [str(photo_dict['csrf']),photo_dict['load_id']]
                mysql.cud(csrf_url,params)

                print("*" + photo_dict['load_num'] + "存入完成")
            except:
                print("csrf存入异常")
        else:
            if is_second:
                break
            time.sleep(35)
            # 如果20s后queue还为空结束线程
            is_second = True





def main():
    sto_page_thread = threading.Thread(target=sto_page)
    sto_result_thread = threading.Thread(target=save_result_mysql)
    sto_page_thread.start()
    time.sleep(10)
    sto_result_thread.start()

    time.sleep(60)
    sto_load_thread = threading.Thread(target=sto_load)
    save_csrf_mysql_thread = threading.Thread(target=save_csrf_mysql)
    sto_load_thread.start()
    time.sleep(30)
    save_csrf_mysql_thread.start()

if __name__ == "__main__":
    main()



