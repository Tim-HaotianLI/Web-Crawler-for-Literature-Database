# 以下内容的设置在：File->Editor->File and Code Templates->python script

# -*- coding = utf-8 -*-
# @time : 2023/10/10 15:39
# @Author : 
# @File : 3.2 getmetadata_ASCE.py
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
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--blink-settings=imagesEnabled=False")
    # options.add_argument("--disable-gpu")
    # browser = webdriver.Chrome(chrome_options=options)
    ## 使用selenium有头战士
    browser = webdriver.Chrome(chromeDrivePath)
    browser.get(url)
    time.sleep(10)

    keywords = []
    try:
        keywords_str = browser.find_element(by=By.XPATH, value='//head//meta[@name="keywords"]').get_attribute("content")
        keywords = keywords_str.split(",")
    except:
        print(f"No author given keywords: {url}")

    try:
        keywords_items = browser.find_elements(by=By.XPATH, value='//div[@class="keywords"]//a')
        for item in keywords_items:
            kw = item.get_attribute("innerText")
            keywords.append(kw)
    except:
        print(f"No official given keywords: {url}")

    browser.quit()
    return keywords

class MyThread(Thread):
    def __init__(self,info):
        Thread.__init__(self)
        self.info = info
    def run(self):
        url = self.info.get("doi")
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
    with open("../results/2.3 paperDetails_ASCE_article.json") as fp:
        infoDict = json.loads(fp.read())

    for k, v in infoDict.items():
        query = k
        infoDetails = v

    numberOfItems = infoDetails.get("numberOfItems")
    content = infoDetails.get("content")

    content_update = []
    content_transfer = []
    # for k,v in tqdm(content.items()):
    #     url = v.get("doi")
    #     keywords = get_data(url)
    #     v["keywords"] = keywords
    #     content_update.append(v)

    for k,v in tqdm(content.items()):
        ## 处理content里面的内容
        content_transfer.append(v)
        if int(k)%8 == 0 or int(k) == len(content):
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
    with open("../results/2.3 paperDetails_ASCE_article_withKWs.json","w") as fp:
        fp.write(json.dumps(dataInfo))
