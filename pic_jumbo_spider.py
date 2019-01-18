# coding: utf-8

from pic_mysql_help import MysqlHelp
from lxml import etree
import threading
import time
import random
import Queue
import requests
import io
import warnings

# 忽略warning
warnings.filterwarnings("ignore")
queue = Queue.Queue(maxsize=600)
link_queue = Queue.Queue(maxsize=600)
color_queue = Queue.Queue(maxsize=1)

def sort():
    sort_list = []
    f = io.open("pic_jumbo_sorts.txt", "r")
    for sort in f.readlines():
        sort_list.append(sort.replace("\n","").replace(" ","").replace("&","-").lower())
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
        'cookie': '__smVID=bcc1be11972506d4dca0e3ee5605fe3b70acb3f4618a3c8eb847f552db1b0e05; __cfduid=d8272fcb49c0616eebe7f5b51ea3ac0701547790381; _ga=GA1.2.370004533.1547790386; _gid=GA1.2.144085218.1547790386; __smWelcomeMatShown=Fri%20Jan%2018%202019%2013:47:28%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); __smListBuilderShown=Fri%20Jan%2018%202019%2013:47:41%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); __smListBuilderOptOut=true; __smToken=ZZ4CBjFLxygAaBTLBieDSz9E',
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
            html = etree.HTML(text)
            load_lists = html.xpath("//div[@class='tri_img_wrap']//a[@class='tri_img']/@href")
            # print load_lists
            for link in load_lists:
                while True:
                    if not link_queue.full():
                        link_queue.put([link,color])
                        break
                    else:
                        time.sleep(1)
            return page_content.status_code
        else:
            return page_content.status_code
    except Exception, e:
        print("174 lines error")
        print e.message

def get_download_link():
    num = 0
    while True:
        if not link_queue.empty():
            try:
                link = link_queue.get()
                link_content = requests.get(link[0], headers=headers())
                if link_content.status_code == 200:
                    link_text = link_content.text
                    link_html = etree.HTML(link_text)
                    link_loads = link_html.xpath("//div[@class='download_box']/a[@class='button big']/@href")
                    # print link_loads
                    for link_load in link_loads:
                        url = 'https://picjumbo.com/wp-content/themes/picjumbofree/run.php?' + link_load.replace("/","").replace("?","&")
                        # print url

                        while True:
                            if not queue.full():
                                queue.put([url, link[1]])
                                break
                            else:
                                time.sleep(1)
            except:
                print("175 error")
        else:
            time.sleep(1)
            num += 1
            if num > 600:
                print("link结束")
                break


def save_to_mysql():
    num = 0
    save_num = 0
    mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
    while True:
        if not queue.empty():
            try:
                save_num += 1
                load_url = queue.get()
                save_url = 'insert ignore into pic_jumbo(load_url,sorts) values(%s,%s)'
                params = [load_url[0],load_url[1]]
                mysql.cud(save_url,params=params)
                print(str(save_num) + "储存结束")
            except Exception,e:
                print "88 error"
                print e.message
        else:
            time.sleep(2)
            num += 1
            if num > 1000:
                print("存储结束或网络超时")
                exit()

def loads():
    color = color_queue.get()
    isbreak = 0
    for num in range(1,10000):
        time.sleep(1)
        print(color + " : " + str(num))

        if color == "latest-free-stock-photos":
            url = 'https://picjumbo.com/latest-free-stock-photos/page/' + str(num) + '/'
        else:
            url = 'https://picjumbo.com/free-stock-photos/' + color + '/page/' + str(num) + '/'
        # print url
        # print url
        status_code = get_second_end_page(url, color)

        if status_code != 200:
            isbreak += 1
            if isbreak>2:
                print color + " stop --------------------->"
                exit()

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

    time.sleep(0.2)
    color_queue.put('latest-free-stock-photos')
    new_Thread = threading.Thread(target=loads)
    new_Thread.start()


    for i in range(6):
        link_Thread = threading.Thread(target=get_download_link)
        link_Thread.start()
        time.sleep(0.2)

    print("开始存数据")
    save_Thread_1 = threading.Thread(target=save_to_mysql)
    save_Thread_1.start()
    save_Thread_2 = threading.Thread(target=save_to_mysql)
    save_Thread_2.start()
    save_Thread_3 = threading.Thread(target=save_to_mysql)
    save_Thread_3.start()
    print("主线程在这")

def test():
    url = 'https://picjumbo.com/wp-content/themes/picjumbofree/run.php?download&d=christmas-shopping-free-photo.jpg&n=christmas-shopping-bags'
    page_content = requests.get(url, headers=headers())
    print page_content.text
    print page_content.status_code

if __name__ == '__main__':
    main()
    # test()
    # print sort()