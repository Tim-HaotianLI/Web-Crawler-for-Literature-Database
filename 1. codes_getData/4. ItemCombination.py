# 以下内容的设置在：File->Editor->File and Code Templates->python script

# -*- coding = utf-8 -*-
# @time : 2023/10/10 17:20
# @Author : 
# @File : 4. ItemCombination.py
# @Software : PyCharm


import json
import jsonpath

def titleKey(Dict):
    newDict = {}
    for _,v in Dict.items():
        content = v.get("content")
    for k,v in content.items():
        title = v.get("title")
        newDict[title] = v

    return newDict

def numKey(Dict):
    newDict = {}
    for i,(_,v) in enumerate(Dict.items()):
        newDict[f"{i+1}"] = v
    return newDict

if __name__ == "__main__":
    with open("../results/paperDetails_WOS_withKWs.json", 'r') as fp:
        wosDict = json.loads(fp.read())
    with open("../results/paperDetails_ELSEVIER.json", 'r') as fp:
        elsevierDict = json.loads(fp.read())
    with open("../results/paperDetails_ASCE_withKWs.json", 'r') as fp:
        asceDict = json.loads(fp.read())

    wosDict = titleKey(wosDict)
    elsevierDict = titleKey(elsevierDict)
    asceDict = titleKey(asceDict)

    for k,v in elsevierDict.items():
        keywords = v.get("keywords")
        if wosDict.get(k) is not None:
            wosDict.get(k).get("keywords").extend(keywords)
        else:
            wosDict[k] = v
    for k,v in asceDict.items():
        keywords = v.get("keywords")
        if wosDict.get(k) is not None:
            wosDict.get(k).get("keywords").extend(keywords)
        else:
            wosDict[k] = v

    newDict = numKey(wosDict)
    newDict_list = [v for _,v in newDict.items()]
    sorted_newDict = sorted(newDict_list,key = lambda x:x["title"])
    newDict = {f"{i+1}":v for i,v in enumerate(sorted_newDict)}
    num = len(newDict)

    dataInfo = {
        "numberOfItems":num,
        "content":newDict
    }

    with open("../results/combinedResults.json","w") as fp:
        fp.write(json.dumps(dataInfo))