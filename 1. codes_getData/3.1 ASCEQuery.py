# 以下内容的设置在：File->Editor->File and Code Templates->python script
import time
# -*- coding = utf-8 -*-
# @time : 2023/8/24 16:26
# @Author :
# @Software : PyCharm


import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium import webdriver
import undetected_chromedriver as uc
from lxml import etree
import json

class My_Chrome(uc.Chrome):
    def __del__(self):
        pass


class ASCEQuery():

    # base_url = "https://ascelibrary.org/search/advanced?"
    base_url = "https://ascelibrary.org/action/doSearch?"


    params = {
        'field1': 'Abstract', # 对全文检索使用AllField; 对Abstract检索使用Abstract
        'text1': None,
        'pageSize': 100,
        'startPage': 0,
        'AfterYear':1956,
        'BeforeYear':2023,
        'sortBy': 'Earliest',
        "ContentItemType": 'research-article'
    }
    queries = []
    numOfQueries = 0
    queriesDict = {}
    countPerQuery = 1

    def __init__(self,):

        self.browser = self.generateBrowser()

    def generateBrowser(self):
        # option = webdriver.ChromeOptions()
        # option.add_experimental_option("detach",False)

        browser = My_Chrome()
        return browser

    def doQuery(self,query):
        queries.append(query)
        self.params["text1"] = query
        self.numOfQueries += 1
        self.queriesDict[query] = {"id": self.numOfQueries, "content": {}}

        data = urllib.parse.urlencode(self.params)
        url = self.base_url + data

        self.browser.get(url)

        numOfItems = int(self.browser.find_element(by=By.XPATH, value='//span[@class="result__count"]').get_attribute(
            "innerText"))
        self.queriesDict[query] = {"id": self.numOfQueries,"numberOfItems":numOfItems, "content": {}}

        print(f"numOfItems:{numOfItems}")

        flag = True


        while flag:

            items = self.browser.find_elements(by=By.XPATH, value='//div[@class="issue-item__content"]')


            self.getMetaData(query,items)

            if len(items) < 100:
                break

            next_page_info = self.browser.find_element(by=By.XPATH,value='//nav[@class="pagination"]/span[2]')
            next_page_text = next_page_info.get_attribute("class")
            print("next_page_text: ",next_page_text)




            if 'disabled' in next_page_text:
                flag = False
            else:
                next_page_button = next_page_info.find_element(by=By.XPATH,value="./a")

                self.browser.execute_script("arguments[0].click()",next_page_button)


        self.countPerQuery = 1


    def getMetaData(self,query,items):

        for item in items:

            title = item.find_element(by=By.XPATH, value='.//h5').get_attribute("innerText")

            try:
                pubyear = item.find_element(by=By.XPATH,value='./div[@class="issue-item__header"]/span[last()]').get_attribute("innerText").split(", ")[1]
            except:
                print("pubyear")
                continue

            journal = item.find_element(by=By.XPATH,value = ".//div[@class='issue-item__body']/p/span[1]").get_attribute("innerText").split(",")[0]
            if journal == "GEOSTRATA Magazine":
                print("journal")
                continue


            doi = item.find_element(by=By.XPATH,value='.//div[@class="issue-item__title"]/a').get_attribute("href")
            try:
                abstract = item.find_element(by=By.XPATH,value='.//div[@class="accordion__content"]/p').get_attribute("innerText")
            except:
                abstract = ""

            self.queriesDict[query]["content"][self.countPerQuery] = {"doi":doi,"journal":journal,"title": title,"pubyear":pubyear,"abstract": abstract}
            self.countPerQuery +=1


    def exportData(self):
        with open("../results/2.3 paperDetails_ASCE_article.json","a") as fp:
            fp.write(json.dumps(self.queriesDict))

if __name__ == "__main__":
    queries = [
        # '"Construction Industry" AND ("Computer Vision" OR "Deep Learning" OR "Machine Learning")'
        '("computer vision" OR "machine vision" OR "vision*" OR "visual *") AND ("construction*" OR "infrastructure*" OR "civil engineering" )',
    ]

    Q = ASCEQuery()
    Q.doQuery(queries[0])
    Q.exportData()

