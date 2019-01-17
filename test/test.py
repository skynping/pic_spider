# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')#上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
driver = webdriver.Chrome(chrome_options=chrome_options)


# driver = webdriver.PhantomJS()

driver.get("https://www.pexels.com/popular-photos/all-time/")

driver.save_screenshot("baidu.png")


driver.close()
driver.quit()