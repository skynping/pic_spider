# coding: utf-8

from pic_mysql_help import MysqlHelp
import threading
import time
import random
import Queue
import requests
import io
import warnings
import json

# 忽略warning
warnings.filterwarnings("ignore")
queue = Queue.Queue(maxsize=600)
color_queue = Queue.Queue(maxsize=2)

def sort():
    sort_list = []
    f = io.open("pic_unsplash_sorts.txt", "r")
    for sort in f.readlines():
        sort_list.append(sort.replace("\n","").replace(" ","-").strip().lower())
    return sort_list

def headers():
    headers = [
        # safari 5.1 – MAC
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",

        # Firefox 38esr
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",

        # # IE 11
        # "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        #
        # # IE 9.0
        # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
        #
        # # Firefox 4.0.1 – MAC
        # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",

        # Firefox 4.0.1 – Windows
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",

        # # Opera 11.11 – MAC
        # "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        #
        # # Opera 11.11 – Windows
        # "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        #
        # # Chrome 17.0 – MAC
        # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        #
        # # 傲游（Maxthon）
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        #
        # # 腾讯TT
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        #
        # # 世界之窗（The World） 2.x
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        #
        # # 世界之窗（The World） 3.x
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        #
        # # 搜狗浏览器 1.x
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        #
        # # 360浏览器
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        #
        # # Avant
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        #
        # # Green Browser
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",

        # Opera
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60Opera / 8.0(Windows NT 5.1;U;en)",
        # "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",

        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",

        # Safari
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",

        # chrome
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",

        # # 360
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        # "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        #
        # # 淘宝浏览器
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        #
        # # 猎豹浏览器
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",

        # QQ浏览器
        # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        #
        # # sogou浏览器
        # "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        #
        # # maxthon浏览器
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        #
        # # UC浏览器
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",

    ]
    num = random.randint(0, len(headers) - 1)
    header = {
        'cookie': 'ugid=d15236715777f0d90f794c70d48cb1d65159266; _ga=GA1.2.716909876.1547779929; _gid=GA1.2.1828923370.1547779929; uuid=0cb59c70-1acc-11e9-b572-61cac541828d; xpos=%7B%7D; _sp_ses.0295=*; _sp_id.0295=f320c93a-e347-4a07-9abe-ea4569f0f248.1547779929.3.1547814862.1547790004.c9363dd6-0453-49e0-bf9d-567cdc6a0967',
        'user-agent': headers[num]
        # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    return header

def get_second_end_page(url,color):
    # page_content = requests.get(url, headers=headers())
    try:
        page_content = requests.get(url, headers=headers())
        if page_content.status_code == 200:
            text =  page_content.text
            json_text = json.loads(text)
            text_lists = json_text['results']
            for text_list in text_lists:
                while True:
                    if not queue.full():
                        queue.put(text_list)
                        break
                    else:
                        time.sleep(1)
            return page_content.status_code
        else:
            return page_content.status_code
    except Exception, e:
        print("174 lines error")
        print e.message

def save_to_mysql():
    num = 0
    save_num = 0
    mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    while True:
        if not queue.empty():
            try:
                save_num += 1
                text_list = queue.get()

                img_id = text_list['id']
                created_at = text_list['created_at']
                updated_at = text_list['updated_at']
                width = text_list['width']
                height = text_list['height']
                color_ = text_list['color']
                description = text_list['description']
                urls_raw = text_list['urls']['raw']
                urls_full = text_list['urls']['full']
                urls_regular = text_list['urls']['regular']
                urls_small = text_list['urls']['small']
                urls_thumb = text_list['urls']['thumb']
                download_link = text_list['links']['download']
                likes = text_list['likes']
                user_name = text_list['user']['name']
                photo_tags = ''
                for tag in text_list['photo_tags']:
                    photo_tags += ' ' + tag['title']

                save_url = 'insert ignore into pic_unsplash(img_id, created_at, updated_at, width, height, color_, description, urls_raw,urls_full, urls_regular, urls_small, urls_thumb, download_link, likes, user_name,photo_tags) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                params = [img_id, created_at, updated_at, width, height, color_, description, urls_raw,
                                 urls_full, urls_regular, urls_small, urls_thumb, download_link, likes, user_name,
                                 photo_tags]
                mysql.cud(save_url,params=params)
                print(str(save_num) + "储存结束")
            except Exception,e:
                print "188 error"
                print e.message
        else:
            time.sleep(2)
            num += 1
            if num > 1000:
                print("存储结束或网络超时")
                exit()

def get_total_page(sort):
    url = 'https://unsplash.com/napi/search/photos?query=' + sort + '&xp=&per_page=20&page=4'
    total_res = requests.get(url, headers=headers())
    if total_res.status_code == 200:
        total_text = total_res.text
        total_page = json.loads(total_text)
        return total_page['total_pages']
    else:
        return

def loads():
    color = color_queue.get()

    # 获取最大页码
    max_page = get_total_page(color)
    get_max_page_times = 0
    while not max_page:
        max_page = get_total_page(color)
        get_max_page_times += 1
        if get_max_page_times > 5:
            max_page = 5
            break

    print(color + " --> " + str(max_page))

    for num in range(1,max_page+1):
        time.sleep(1)
        print(color + " : " + str(num))
        url = 'https://unsplash.com/napi/search/photos?query=' + color + '&xp=&per_page=20&page=' + str(num)
        get_second_end_page(url, color)
        print(color + " : " + str(num) + " over")

def main():
    # 按分类爬取
    sort_lists = sort()
    for color in sort_lists:
        # print color
        color_queue.put(color)
        color_Thread = threading.Thread(target=loads)
        time.sleep(0.2)
        color_Thread.start()

    print("开始存数据")
    for i in range(6):
        save_Thread_1 = threading.Thread(target=save_to_mysql)
        save_Thread_1.start()
        time.sleep(0.2)
    print("主线程在这")


if __name__ == '__main__':
    main()

