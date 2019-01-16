#coding: utf-8

from pic_getIndexHtml import page_spider
from lxml import etree
from pic_mysql_help import MysqlHelp
import time
import random
import requests
import os

class sto_load:
    def __init__(self,):
        self.headers = self.__headers()

    def __headers(self):
        headers = [
            # safari 5.1 – MAC
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",

            # Firefox 38esr
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",

            # IE 11
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",

            # IE 9.0
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",

            # Firefox 4.0.1 – MAC
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",

            # Firefox 4.0.1 – Windows
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",

            # Opera 11.11 – MAC
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",

            # Opera 11.11 – Windows
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",

            # Chrome 17.0 – MAC
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",

            # 傲游（Maxthon）
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",

            # 腾讯TT
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",

            # 世界之窗（The World） 2.x
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",

            # 世界之窗（The World） 3.x
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",

            # 搜狗浏览器 1.x
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",

            # 360浏览器
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",

            # Avant
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",

            # Green Browser
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",

            # Opera
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60Opera / 8.0(Windows NT 5.1;U;en)",
           "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
           "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",

           # Firefox
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
           "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",

           # Safari
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",

           # chrome
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
           "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",

           # 360
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",

           # 淘宝浏览器
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",

           # 猎豹浏览器
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
           "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
           "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",

           # QQ浏览器
           "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
           "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",

           # sogou浏览器
           "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",

           # maxthon浏览器
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",

           # UC浏览器
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",

        ]
        num = random.randint(0,len(headers)-1)
        return headers[num]

    def load(self,csrf,photoId,num):
        url = 'https://stocksnap.io/photo/download'
        # pre_data = {'_csrf': 'OB1nHn4t-2koKPWonzGFKpK-cn368KZKuSJI', 'photoId': '3MRNL2SKAJ'}
        pre_data = {'_csrf': csrf, 'photoId': photoId}
        headers = {
            'cookie':'__cfduid=dec1fafd2cdc925b1bb9601463f5083631547627168; _csrf=Ba5YQYnk8E_Et1sLT-xWOw_V; _ga=GA1.2.408303191.1547627176; _gid=GA1.2.1848125566.1547627176; _omappvp=C3NFshqoDF1V82KXk0G3XrlDO8tFHwrapB8Obm7vH8nFLqCQQvilYe2tw9dipq880ZffQtzYw7EXnaSMnE9DVxIlFPXnYcoG; photoDownloads=0B0ML69LXH%2C6Y5SVWDPHG%2CORQQTOGWRO%2CCCKYDDOYQ9; _gat=1; photoViews=LWSE2FEO65%2C08YYDJEUCY%2C0B0ML69LXH%2C6Y5SVWDPHG%2CORQQTOGWRO%2CCCKYDDOYQ9%2CVQT82JJSPU',
            'user-agent': self.headers,
        }
        reponse = requests.post(url, data=pre_data, headers=headers, stream=True)
        file = reponse.content
        print reponse.status_code
        with open("./pic_sto/"+"pic_" + str(num) + "_" + photoId + ".jpg", "wb") as f:
            f.write(file)

    @classmethod
    def makedir(self, filepath):
        isExists = os.path.exists(filepath)
        if isExists:
            return False
        else:
            os.makedirs(filepath)
            return True

    def get_scrf(self,id):
        time.sleep(random.randint(1, 3))
        load_url = "https://stocksnap.io/photo/" + id
        load_spider = page_spider(url=load_url)

        load_text = load_spider.get()['text']
        # 转换成xpath格式
        load_html = etree.HTML(load_text)
        # 筛选
        csrf = load_html.xpath("//div[@class='equal-columns']//form/input[1]/@value")[0]
        return csrf.strip().encode("utf-8")

    # 获取id列表
    def get_id(self,downloads):
        mysql = MysqlHelp(db="sky_pic", host="localhost", port=3307)
        url = "select img_id from pic_stocksnap where downloads > %s"
        params = [downloads]
        return mysql.all(url,params=params)

def test():
    sto = sto_load()
    sto.load('rQWXtAp5-t8cFMjxoFcNQZHsziBfh8AA3zFA','XHT8C9KTXD')

def main():
    # downloads = str(input("保存下载量至少为："))
    downloads = "0"
    num = 0
    sto_load.makedir("./pic_sto")
    sto = sto_load()
    id_lists = sto.get_id(downloads)
    csrf = 'rQWXtAp5-t8cFMjxoFcNQZHsziBfh8AA3zFA'
    for id, in id_lists:
        num += 1
        print "==" + id + " downloading" + "=="
        sto.load(csrf,id,num)
        print "=="+id + " download over" + "=="


if __name__ == "__main__":
    main()
