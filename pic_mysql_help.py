# coding: utf-8
# 包网：https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python

from MySQLdb import *


class MysqlHelp:
    def __init__(self,db,host='47.107.94.194', port=3306, user='root', passwd='ubuntu', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.db = db

    def open(self):
        self.conn = connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
        self.cursorl = self.conn.cursor()

    def close(self):
        self.cursorl.close()
        self.conn.close()

    # 修改
    def cud(self, sql, params=[]):
        try:
            self.open()
            # print u"设置中--"
            self.cursorl.execute(sql, params)
            # print u"设置结束"
            self.conn.commit()

            self.close()
            # print u"设置成功"
        except Exception,e:
            print e.message

    # 查询
    def all(self,sql, params=[]):
        try:
            self.open()

            self.cursorl.execute(sql, params)
            result = self.cursorl.fetchall()

            self.close()
            return result
        except Exception, e:
            print e.message

def main():
    while True:
        print "*"*60
        print u"功能"
        print u"1.退出"
        print u"2.查询"
        print u"3.修改"
        target = raw_input("输入功能：".decode("utf-8").encode("utf-8"))

        try:
            int(target)
        except:
            print u"你在逗我"
            continue

        # print len(target)
        # if len(target) > 1:
        #     print u"你在逗我"
        #     continue
        if int(target) == 1:
            break
        db = 'python3'
        helper = MysqlHelp(db)
        if int(target) == 2:
            # sql = 'select name,country,ranking from top_500 where id<5'
            sql = raw_input("请输入查询指令：".decode("utf-8").encode("utf-8"))
            # print helper.all(sql)
            try:
                for i in helper.all(sql):
                    # print i
                    print "-" * 100
                    print i[0].encode("utf-8") + " | " + i[1].encode("utf-8") + " | " + str(i[2]) + "\t"
                    print "-" * 100
            except:
                print u"输入有误，请重新输入"
                continue
        elif int(target) == 3:
            sql = raw_input("请输入修改指令：".decode("utf-8").encode("utf-8"))
            helper.cud(sql)
        else:
            print u"你在逗我"

if __name__ == "__main__":
    main()
