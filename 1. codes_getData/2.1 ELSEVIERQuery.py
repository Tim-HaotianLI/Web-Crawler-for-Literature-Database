# 以下内容的设置在：File->Editor->File and Code Templates->python script

# -*- coding = utf-8 -*-
# @time : 2023/8/23 22:08
# @Author :
# @Software : PyCharm

import urllib.request
import urllib.parse
import json
import time
from tqdm import tqdm

class ELSEVIERQuery():
    ESV_API_KEYs = {
      "public": "7f59af901d2d86f78a1fd60c1bf9426a",
      "private":"96c3f3332c6c08575bf98a4353257acd"
    }
    ESV_INIS_KEY = "23c740ed9db07b231df869be5c4675fd"
    urls = {
        "scienceDirect":"https://api.elsevier.com/content/search/sciencedirect?",
        "scopus":"https://api.elsevier.com/content/search/scopus?",
        "doi_details":"https://api.elsevier.com/content/article/doi/"
    }

    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': '96c3f3332c6c08575bf98a4353257acd',
        'X-ELS-Insttoken': '23c740ed9db07b231df869be5c4675fd',
        'Cookie': '__cf_bm=IX_jZvp0iAHT4CkEBRGsObkqQPSbrT4hb4N2X0GqYcA-1692855251-0-AdH6o8HqCucxDlWV6JTP1HmJdDRKZUH+MFmu3HCyv4IY2xEOBZxPrCRAgKe0jEzta9wlnDzS3kQtvJm9XwYr1o4='
    }
    step = 0
    queryDict = {}
    queries = []
    length = 0

    def __init__(self,database,key=None):
        if database.lower() == "sciencedirect":
            self.url = self.urls.get("scienceDirect")
            self.step = 100
        elif database.lower() == "scopus":
            self.url = self.urls.get("scopus")
            self.step = 25

        if key is not None:
            self.ESV_API_KEYs["private"] = key

        self.key = self.ESV_API_KEYs["private"]

    def setPrivateKey(self,key=None):
        self.ESV_API_KEYs["private"] = key

    def getQueryNum(self,query,key):

        print(query)

        data = {
            "query": f'TITLE-ABS-KEY({query}) AND PUBYEAR > 1922 AND PUBYEAR < 2024 AND SRCTYPE(J) AND SUBJAREA(ENGI) AND DOCTYPE(AR) AND LANGUAGE(English)',
            "apiKey": key,
            "insttoken": self.ESV_INIS_KEY,
        }
        data = urllib.parse.urlencode(data)
        url = self.url + data
        url = url.replace("+", "%20")

        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")
        content = json.loads(content)
        length = content["search-results"]["opensearch:totalResults"]
        return int(length)

    def getMetaDataFromElsevier(self, numOfItems, query, date=None):
        self.length += 1
        queries.append(query)

        total = self.getQueryNum(query,self.key)
        time.sleep(1)

        size = total if numOfItems<total else numOfItems

        result = []

        print(f"size:{size}")
        cursor = "*"

        for start in tqdm(range(0,size,self.step)):
            data = {
                "query": f"TITLE-ABS-KEY({query}) AND PUBYEAR > 1922 AND PUBYEAR < 2024 AND SRCTYPE(J) AND SUBJAREA(ENGI) AND DOCTYPE(AR) AND LANGUAGE(English)",
                "apiKey": self.key,
                "insttoken": self.ESV_INIS_KEY,
                "count": self.step,
                "cursor":cursor,
                # "start": start,
                "view":"COMPLETE"
                # "articleTypes":"REV"
            }
            data = urllib.parse.urlencode(data)
            url = self.url + data
            request = urllib.request.Request(url=url,headers=self.headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode("utf-8")

            r,c = self.parseMetadata(content)
            result.extend(r)
            cursor = c
            time.sleep(2)

        results = {"totalQueries":size}
        for i,query in enumerate(result):
            results[str(i+1)] = query

        with open(f"../results/2.2 infolist_Elsevier_article_1.json","w") as fp:
            fp.write(json.dumps(results))

    def parseMetadata(self,content):
        data = json.loads(content)
        cursor = data["search-results"]["cursor"].get("@next")
        data = data["search-results"]["entry"]
        return data,cursor

    def extractingDOI(self):
        with open("../results/infolist2_Elsevier_1.json","r") as fp:
            content = fp.read()
        data = json.loads(content)
        dois = []
        for k,v in data.items():
            if k == "totalQueries":
                continue
            else:
                dois.append(v.get("prism:doi"))

        dois = list(filter(None,dois))

        print(dois)


    def parseQueryData(self):
        with open("../results/2.2 infolist2_Elsevier_article_1.json","r") as fp:
            content = fp.read()

        data = json.loads(content)
        doi = data["1"]["prism:doi"]
        doi_url = self.urls["doi_details"]
        url = doi_url+doi
        self.headers["X-ELS-APIKey"] = self.ESV_API_KEYs["private"]
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")

        with open("../results/testing2_details.json","w") as fp:
            fp.write(content)




if __name__ == "__main__":
    queries = [
        # '"construction*" AND "computer vision"',
        # 'computer vision AND "construction*"' # 用于进行review的检索
        '( "computer vision" OR "machine vision" OR "vision*" OR "visual *" ) AND ( "construction*" OR "infrastructure*" OR "civil engineering" )' # 用于进行article的检索
    ]
    '''
    参考文档：
    https://dev.elsevier.com/documentation/ScopusSearchAPI.wadl
    https://dev.elsevier.com/sc_search_tips.html
    '''

    Q = ELSEVIERQuery("scopus")
    Q.getMetaDataFromElsevier(500, queries[0])
    # Q.extractingDOI()
