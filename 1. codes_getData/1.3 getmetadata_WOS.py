# 以下内容的设置在：File->Editor->File and Code Templates->python script
import threading
# -*- coding = utf-8 -*-
# @time : 2023/10/10 10:17
# @Author : 
# @File : 1.3 getmetadata_WOS.py
# @Software : PyCharm

import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import jsonpath
from tqdm import tqdm
from threading import Thread

def get_data(url):
    chromeDrivePath = "./chromedriver.exe"
    ## 使用selenium无头骑士
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--blink-settings=imagesEnabled=False")
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(chrome_options=options)
    # browser = webdriver.Chrome(chromeDrivePath)
    browser.get(url)
    time.sleep(10)
    keywords_items = browser.find_elements(by=By.XPATH, value='//a[contains(@id,"FRkeywordsTa")]/span')
    keywords = []
    for item in keywords_items:
        keywords.append(item.get_attribute("innerText"))

    browser.quit()
    return keywords

class MyThread(Thread):
    def __init__(self,info):
        Thread.__init__(self)
        self.info = info
    def run(self):
        base_url = "https://www.webofscience.com/wos/woscc/full-record/"
        wos_id = self.info.get("wos_id")
        url = base_url + wos_id
        keywords = get_data(url)
        self.info["keywords"] = keywords
        self.result = self.info


def multi_threading(infos):
    threads = []

    for info in infos:
        t = MyThread(info)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return [thread.result for thread in threads]



if __name__ == "__main__":
    dataInfo = {}
    with open("../results/2.1 paperDetails_WOS_article_1.json") as fp:
        infoDict = json.loads(fp.read())

    for k, v in infoDict.items():
        query = k
        infoDetails = v

    numberOfItems = infoDetails.get("numberOfItems")
    content = infoDetails.get("content")

    content_update = []
    content_transfer = []
    for k,v in tqdm(content.items()):
        ## 处理content里面的内容
        content_transfer.append(v)
        if int(k)%10 == 0 or int(k) == len(content):
            content_update.extend(multi_threading(content_transfer))
            content_transfer = []

    print(f"数据量：{len(content_update)}")
    print(content_update)

    for i, c in enumerate(content_update):
        content[f"{i+1}"] = c

    dataInfo["data"] = {
        "query":query,
        "numberOfItems":numberOfItems,
        "content":content
    }
    with open("../results/2.1 paperDetails2_WOS_article_withKWs.json","w") as fp:
        fp.write(json.dumps(dataInfo))
