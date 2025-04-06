# 以下内容的设置在：File->Editor->File and Code Templates->python script

# -*- coding = utf-8 -*-
# @time : 2023/8/23 9:35
# @Author :
# @Software : PyCharm

'''
    该类的说明：
        这个类的作用是：只需要输入查询语句，就能够将查询的结果所有的MetaData都输出为json文件。
        但是，这个代码的作用仅仅知识输出json文件，对MetaData的处理，需要进一步的代码实现。
    该类的业务逻辑：
        1. 只生成一个SID                 √
        2. 对于每一个Query指定生成qid     √
        3. 对每一个生成的content都进行分解后输出到JSON文件 √
'''

import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import json


class WOSQuery():
    headers = {
            'Accept': 'application/x-ndjson',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Cookie': 'OptanonAlertBoxClosed=2022-09-28T02:38:47.267Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Feb+14+2023+18%3A36%3A36+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.39.0&isIABGlobal=false&hosts=&consentId=ff159777-d898-4ec3-9a0e-ef4f9a82af53&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0002%3A1&geolocation=HK%3BHCW&AwaitingReconsent=false; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; group=group-f; _abck=D15A1F2ED8AC97C2FC9322F7591CF72B~0~YAAQN/AoF0nvyvOJAQAA14DmGwqR0LdWm2SlktIWP2OQJ3L06yibUNIvfe6YdA9W09NXRDY36xgSCeTOGLDN7nDN9NtJ+eZJ44y5tnM5j7NepEGdZrzihG4guzOBMmBocRfvcdG8LveMzm/DwvljLCZNR3frdPdfzcmfH+d87r2aaUmCOawjPHigAaaXr2qdNw1/qJAsoPoZSejouk98wnYS+hzKEZo7vjOd6C6sZO8MIlWEqYrrK9zWorSxCEoMQyOSvdOr6Zyd9o3jj3lLris1+sj2RRVZZPus7NRN015bPoife+83qKwXsdZRuJpum4IdIhxc0yRfhc7JovrPqrh+oEqZTh4PBX8H54GSzk7namsiZkSi+AtPh7IM+pFiqsAToYlUOyBUkHBiqR/AFJuxN90eamCja/3oGqVi~-1~-1~-1; bm_sz=02EE5B18F78DF749E60171F1C09674A9~YAAQN/AoF0rvyvOJAQAA14DmGxQ86Ojx5J9k3erhCii71m6Tj6ODlhfWTGMJWWlW0d6fLlFEVpqmIfcspaaidPMBYjoQyAlyaQTTf/szOBNkBrj9wlL+izgmnq6aNmjxtNCIOfMmmD0L3zaaSusHAl06y2V2v4zgQmHwl5ke1WVXvUw1pxsqoCiifM7pkL7pyBo4Cxh5nx4JNkPtN/94EGuQT8feFS5UCCQKagTCEhs3gQ+Rte98mIe/ZHjtAIJlwcFFL7Dl/sd4y3dUT/CA8F6fQ3bInVjNDc3Rl8Qgg+2ZCPTRNHAE6d4=~3290936~3551284; _sp_ses.840c=*; RT="z=1&dm=www.webofscience.com&si=54768a18-9816-4198-9ce4-aaf11c95721c&ss=llm12y4c&sl=1&tt=2dn&bcn=%2F%2F684d0d4c.akstat.io%2F&ld=29rww"; _sp_id.840c=99c61b0c-c371-4e47-933a-c2a0eeb4b374.1664332715.133.1692695765.1676370996.d21bae6c-bb56-4b2f-b50d-b8006a79eee4.e30f5c42-1029-4e56-aada-7073aa42ab45.91472012-8cb2-45ef-b3c1-3b4c48d8518b.1692687520914.106',
            'Origin': 'https://www.webofscience.com',
            'Referer': 'https://www.webofscience.com/wos/woscc/summary/ea4f1d55-4a94-437e-9705-bb75e34d6444-9f1160a6/relevance/1',
            'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
    search_baseURL = "https://www.webofscience.com/wos/woscc/advanced-search" # 该链接用于进行高级检索
    queryDict = {}
    queries = []
    length = 0

    def __init__(self, chromeDrivePath):
        self.chromeDrivePath = chromeDrivePath
        self.browser = self.generateBrowser()
        self.browser.get(self.search_baseURL)
        time.sleep(5)
        # cookies_button = self.browser.find_element(by=By.XPATH,value="onetrust-accept-btn-handler")
        # cookies_button.click()

        self.baseHandler = self.browser.current_window_handle
        self.sid = self.parseSID()
        self.wos_baseURL = f"https://www.webofscience.com/api/wosnx/core/runQueryGetRecordsStream?SID={self.sid}" # 该链接用于进行文献的matadata获取

    def generateBrowser(self):
        # 该函数用于生成selenium的browser对象
        browser = webdriver.Chrome(self.chromeDrivePath)
        return browser

    def parseSID(self):
        # 该函数用于解析网页中的SID
        # 注：SID是登录WOS的账号
        self.browser.switch_to.window(self.baseHandler)
        js_session = "return window.sessionData.BasicProperties.SID"
        sid = self.browser.execute_script(js_session)
        return sid

    def getSID(self):
        # 该函数用于返回SID
        return self.sid

    def parseQID(self,queryStr):
        # 该函数用于解析网页中的QID
        # 注：QID是每一个查询语句的独立身份
        self.length = self.length + 1
        advanced_search = self.browser.find_element(by=By.XPATH,value="//textarea[contains(@id,'advancedSearchInputArea')]")
        # content = "TS=(computer vision* AND construction site management)"
        self.browser.execute_script("arguments[0].value=''",advanced_search)
        advanced_search.send_keys(queryStr)
        time.sleep(1)

        search_button = self.browser.find_element(by=By.XPATH,value="//button[@data-ta='run-search']")
        self.browser.execute_script("arguments[0].click()", search_button)
        time.sleep(1)

        latest_handle = self.browser.window_handles[-1]
        self.browser.switch_to.window(latest_handle)
        time.sleep(1)

        qid = self.browser.find_element(by=By.XPATH,value="//div[@data-ta='search-info']").get_attribute("data-ta-search-info-qid")
        totalQueries = int(self.browser.find_element(by=By.XPATH,value="//div[@data-ta='search-info']").get_attribute("data-ta-search-info-count"))

        self.queryDict[queryStr] = {"id":self.length,"totalQueries":totalQueries,"qid":qid,"handle":latest_handle}
        self.queries.append(queryStr)

        self.browser.back()
        self.browser.switch_to.window(self.baseHandler)
        time.sleep(1)

    def getQID(self,queryStr):
        # 该函数用于返回指定查询语句的QID
        return self.queryDict.get(queryStr).get("qid")


    def getMetaDataFromWOS(self,queryStr):
        # 该函数用于获取每一个查询语句的MetaData
        id = self.queryDict.get(queryStr).get("id")
        qid = self.getQID(queryStr)
        totalQueries = self.queryDict.get(queryStr).get("totalQueries")
        content = ""
        print("------->totolQueries:",totalQueries)
        for page in range(1,totalQueries+1,50):
            data = '{"qid":"'+qid+'","retrieve":{"first":'+str(page)+',"sort":"relevance","count":50,"jcr":true,"highlight":true,"analyzes":["TP.Value.6","REVIEW.Value.6","EARLY ACCESS.Value.6","OA.Value.6","DR.Value.6","ECR.Value.6","PY.Field_D.6","DT.Value.6","AU.Value.6","DX2NG.Value.6","PEERREVIEW.Value.6"]},"product":"WOSCC","searchMode":"general","viewType":"records","bm-telemetry":"a=&&&e=MDc0N0Y0NDFFQThDQTFDQjk0QkNGMzQ1M0Y2NkIxRUJ+WUFBUWQ0N0lGK1lHQXh1S0FRQUF3QnhySWhURUFiT1R5ZmJkU0xJcTB4emJTRzdVc1YxRFNkUDBId0dzUTNVSFA4NHIva210d0tBRGhNLzRRdytwelRrU1hlWitnMTZrbW5tQTYxVGtrekdiSUhFYUEvUnVQQk8zcC9WekxVVHcxUVhaZTBCQmhqVTkxc0xlbmdMZjBkbUxFM2pRbkJBVkVITWNMdWg1TCtady9FVWhtYWVpRC9MUE5TcVVKalhqWmF3SHhEY2NZbkdoc29QU1FXVHZnMHdiMW4zNitLL0EvL01wUmxuK1gzbFpuUlRvN1VIOUY2NDlUMndrNkdmYW5ITERCQWViWUJHd20xYm9nc2ZHLzJlVFRwSjRGQzN5TUVGTkhabkZGQVhnTXhOaDZiV0lBZjJVU05UVjRUandicDNUaHYyd0EyUTlQOE0rS3BMUnVNZz1+MzE2MDM5MH4zNDIwNDgz&&&sensor_data=MjszMTYwMzkwOzM0MjA0ODM7NiwxMywwLDAsMiwyNjs9eCFIfmxqMl0/IWlWXjw6dF9eTlVJeko9KkM2S05tOW9jT3lZWFIxVT58fGxtU1g8K1okODpsNTYkMUBMZFElL2MjI3JGRnFFQXNza3tub1lVdFJacUoqKmwvNl1fNDlTQkYoYWI2NmBWQUdZN05UYVsvNWYmSjZUXlZoIFk0TlRUWy8hb0gybFU4O1klL3R5aEwtclBQJCgzfl8zQilLVS06LzZUXk9AKiw1Ql5ScWZoUTJNeGJOVVR8RXc5WXt3TVtAVDZhOSUuQyFLZDVCSHIreyZVWVlYX3xdTX4+Vy9Ha0Uod2VTMEZmUTBdKXNuMiFCRWY1NmZFPV5IZEZvTmpRb2glVlhlKCZMSnUhOHRXcWBxTixdUTtuPlJNczZuOXNRUHkhcF97I0xZIyYxNEZAQiFXTzN2MX04Jl99cl98TkZRJlhbT3QuTnhLbDlNcGN0WiU0Zl5UQGs6ZFUudD9hayZINis5XW5LbE12RV5dIDhpT1p3N15Ueno4TjwjPnMhNX1bYUgwdFMjQyA4dD4qSHh0JTwkNltURSgpNnxOaHoxMGtiY0NpVndkLXgtZzYhdF0+PnNRYTAsdV9PcSpneDRwbzpVLy1uej9kVFEoc35GOkhuVVlKYXU7alpLY3wuLk0+WWtMRWhDLn0xND0vdDJbT1o2dWxyaW10aDJ2VCBGQUBUdWFDczA0Si1iKC9hXk5JdFc+IXh4KD9TWUAyYyUuKU12MCU0bXBWaSByPl5iYS5XLz5OUF9fKXEoRGYve3ZMNF50bWR5Y3A9VDpeLTlGdGBUM3RhZ0M4aVJeQ21teX1MbFNsNnskaHNgWkVKMDtzIClvXjlTO1tgID53QlZgSE4jRGZsXXttc2BYLDxQWEFOSEMxQW8rSiZLR0oxayk4QUV7Q35yWypmY1c3cSRNKmF1cD5Jey5TeWkzRXtxPEQ2Z2VxeHozRUY6TDFuNUQ/dig8bHM/azVOdik7eG1gUTc0fn5BPWhrIys9cmEhREAhPUV1M2Q6bV9dZHZ6aVVPQyg+LSloOjlVZmtafD86YypwT1tJXiRmSiRnLk9OdW00I2RCOk54UHcqN18pVyN0P1t7KUpiYUR9TG0le3t+dHtrLDRvc0drSDZfTEglWVJdMTZ2PyViISNlUEJLISVUKSZ9K1d5TWU9K294PSUkLDEvfWsxUD8hIXgrOGF0V15jZVlyPWJKOzteLCghPXdQNGBbN0k9WElSbl42eClePk9TfUd8TCxdMFV5LDF+X2Z0Uip+UE00dXxnPmp3fG5TZX5MZ0khZ0F3OXNxMDFBa2xGcl15e19sOkBGNU9nUEZgfCBSY0E7YEp+Qy9ZUmcgQmM6Vz4zJkxhZTd3KktIeV9+bTwmbU45LUUqXXsgZy8wRjo2MF5OXVZXKXk5XWFWeyt1SkFud1BEazZNenAsdF4/NjVFVnNIR1E2fWU2NTxaeV5BPHd1JjVvSCFLcHVEalhMVU1eZSEsIXRvP2tzbD5iUDMhSl87Oi85YGEsQGczM1YwPjZVKCMtfHtHLDM4SUA6PUhse10/UG5vQktWZHU1N28oSlt6dWMsYGptUGk1cWpJUUUoU110RG9GOXNPKzAvSktIPCg9K342NVIxR0MsMGp8dz0zQCwoOCovV2M+Qk5teUhxNz9hbHtmQm91UDh0KUVJaGUub3lYUlB0Xk4zVik6ZkFgcU5PX04+Vm1fU0RCN2EjJE9dRUEzRWtXQ1dkQksuUjU8JSQ2IXg/Zl4+RlBmKThXaWh7QFIlejc4SGFMTzRtOGY3UmhdNHhOQi5DRXsmU2QlI0QyIF08dUhuej0weFF1UiF+RCxsMyhwajU3Y3d6XSk5MEpMfFhkSnspdU8tXXt4XXw1OnduWElMcnQ/aUJdLktjYFgwfHt1Tm5JdlMzKCBidFNLLT9yeHRqKF5VMCUkRWhjRVQkaHlvPjFVUTUyaXdCSSxqUDI5bF4oKihhM3EsM15AUzJFe1ZWRykrNF9AZWI3QVpIM1E/bVApWjZhRXQkJjdDJklVO2JlSUgranhxP3s/UTkhVFkoXy96VEEkSSQ6RS8uN3FReHRXYGNZSEl5dTRBLyoqRX4hUCwsIz52WnYhK307MnQtIHx4dyYhLyNLelV4Mz18RFlPX0E5NjokPG0lJj5COzdkei9CYCo2IE9JelRGP09FQjxUYj1udSwjL0MsPD8tXVRVfiV1UVo9aWQmREhzQnZHJitVeTw5bWZeSVtdWjU6JUlmZVA9X09GJjhgVDFWUmxfYHdjLjkjNWdJPilbX1R6NzBYNld7N0xuOW5Pd0whJWEsQG9oXU8qKntkaE42KWtFMCpyV0B4Pj1JbUhNeVsjWG1JKy9leXQ/Y2dtM1ZXJWxURHIoMHJoNT40dWQsVUBMRyZweUEhIGFPfkx1MDojYUp9ST0oLmUtMU9SRl96KkpJKncjREczPi9GbFhxLUV6LDg8ZjlwKXhneTZFUCgud3k5SV8qMUc5SjkgTihDNiUhN3FgPz1uRyNIXlpjPylSWm1lLjhgTFE0Unxuc3h5YUZHc0NYOj0zZjFCMWg6K0MwUHQreFpTWkhieFBrWXxvXWs/QW8xenlmMkNQaXkjQXxjWWc2WS88I0dfZHxONF1VMC9PTjpfbHV2T1VnbCp3K199Xys5OEV8YmJ1UW9RPjV2WzRQQ3olM05YYkE0UiNQK18+Zn41Q3ZhenQxIXZgITkxQC4mN05abiVwaHZqTHNZVG83bG8paEw9cl4zWGBvISw/XjxLI3EwTmNEPTtSJEdPMipeb1F1NlQ9TTF5ZW5uXktUI3F6RXEgQVk5ZE4heFhFbkxpKnlsWVI5Tns0R21PMGh4LFl0bDQocSFTVCRYWV1eYF1OP3ZjLX5hWzI7a0w5bWU/ZDs6My14VWxfTD4qJCY+OzVgWCFQfSsmRyw1QDxmIENrZjgtXUJMXlN6LDBWXkN1QUZHJWQkMEs/XnNYZ2hWQV4zNmRuZER9KFQ+TShxXWNkbCFRKi5uMD1hbCU4SDI5e1dgcE13dV5fS2tVZk48I2NYeWwqLy9WUSk4WGQpJSRnSWB0RXokI3B2OX5OX0c7Vk1mSyYxM1poMkt1LFVIWzcwRl06IFVoNS08T25DSzV5MUE1dTAwWnFMZzBJbyAwcWYoPSxpc3Y7KVZqbXFPVUY3JSR8KERbY0AoID1nbkQ5akh4fkQ5QFAwSVgqcyhpcC5oSj9LdX44OVQ6PzMkSyhddkA8ekFCaXBDWW98PSQjUHljbX0yckslVjxdNU9vZWQ3c1VKbyA9WCY/eCE9LCVWJDF9UGQ9Rl8tJU0pfW9xKjt3fHQ5PH4wYSVQZX0od1MyNzZrL18/W2dWPG82VzhrTnshIXdUN1M5YixEQ2dwJiVFV2c+I1BZOCRlTndIVVFBIShdU25WeF8oa3tLWGg9eThuTiNDbmlTLXFYeDB6L2pMLGk5WisyaT0lSn1fc144LTloSTd7KUhANHohKy9SVCN6dEpwXWl1UnRbNkliRj1YekwqJCg9eihnPykjai94aUJVTz00XltLa2Y5IGBWTChoJWc+MFZzUjJBeWF0V05nT3lPIXp2fkxKZEVdZjBUWWlFM3ZJJkxWWGo2LUovIHxBc0AlS1NkTi0heCplVS1jTHFRWFQpN0tDSDwxTi9fI14qbj9UNkN+fGRKcXY5RXRFTS9OQ1ZeLX42Nnc1YzU1azcgZGdWX1tTSCtVLkdgIU5bSWpgLCtIZCNeZEB6NjY2dGQzWWY0YmRyaDsjMTppSlpVcGlFWXI5KXlzXT1jQEFrOWwlS3h8JHkxekI/IFlLWD1yIEFdXzdqemJS"}'
            print(data)
            data = data.encode("utf-8")

            request = urllib.request.Request(url=self.wos_baseURL, data=data, headers=self.headers)
            handler = urllib.request.HTTPSHandler()
            opener = urllib.request.build_opener(handler)
            response = opener.open(request)
            content += response.read().decode("utf-8")
            # print(content)


        data = self.parseMetaDataFromWOS(queryStr,content)
        with open(f"../results/2.1 infolist_WOS_article_{id}.json","a") as fp:
            fp.write(data)

    def parseMetaDataFromWOS(self,queryStr,content):
        # 该函数用于解析每一个查询语句的MetaData
        pattern = r'\}\n\{'
        results = re.split(pattern,content)
        length = len(results)
        data = {}
        for i,r in enumerate(results):
            if i == 0:
                results[i] = json.loads(r + "}")
            elif i < length-1:
                results[i] = json.loads("{" + r + "}")
            elif i == length - 1:
                results[i] = json.loads("{" + r)

        for d in results:
            if d.get("key") == "searchInfo":
                data["numberOfItems"] = d.get("payload").get("RecordsAvailable")
                data["query"] = queryStr
            if d.get("key") == "records":
                for k, v in d["payload"].items():
                    data[k] = v

        return json.dumps(data)



if __name__=="__main__":
    chromeDrivePath = "./chromedriver.exe"
    Q = WOSQuery(chromeDrivePath)
    SID = Q.getSID()

    queries = [ # 查询语句
        # '(DT=(Review)) AND TS=("Construction Industry" AND ("Computer Vision" OR "Deep Learning" OR "Machine Learning"))',
        # '(DT=(Review)) AND TS=(construction*) AND TS=(computer vision)',
        # '((TS=(computer vision) AND TS=(construction*)) AND DT=(REVIEW)) AND (LA==("ENGLISH") AND SJ==("ENGINEERING" OR "CONSTRUCTION BUILDING TECHNOLOGY" OR "COMPUTER SCIENCE" OR "ARCHITECTURE"))', # 用于进行review的检索
        # 下面这个是我自己的研究
        # '(TS=("computer vision" OR "machine vision" OR "vision*" OR "visual *") AND TS=("construction*" OR "infrastructure*" OR "civil engineering")) AND (LA==("ENGLISH") AND DT==("ARTICLE") AND TASCA==("ENGINEERING CIVIL" OR "CONSTRUCTION BUILDING TECHNOLOGY" OR "ENGINEERING MULTIDISCIPLINARY" OR "COMPUTER SCIENCE INTERDISCIPLINARY APPLICATIONS"))' # 用于进行article的检索
        '(TS=("corporate strategy") AND TS=("capital structure") AND TS=("diversification")'
    ]

    # print("SID:",SID)

    for q in queries:
        Q.parseQID(q)
        print(f"{q}:",Q.getQID(q))
        Q.getMetaDataFromWOS(q)


















