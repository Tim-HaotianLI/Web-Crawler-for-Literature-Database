# 以下内容的设置在：File->Editor->File and Code Templates->python script

# -*- coding = utf-8 -*-
# @time : 2023/10/9 19:37
# @Author : 
# @File : 1.2 WOSParseData.py
# @Software : PyCharm

import json
import jsonpath

dataInfo = {}

if __name__ == "__main__":
    with open("../results/2.1 infolist_WOS_article_1.json","r") as fp:
        infoDict = json.loads(fp.read())

    query = None
    numberOfItems = None
    journals = []
    titles = []
    abstracts = []
    dois = []
    wos_ids = []
    pubyears = []
    for i,(k,v) in enumerate(infoDict.items()):
        if i == 0:
            numberOfItems = v
        elif i == 1:
            query = v
        else:
            journals.append(jsonpath.jsonpath(v,"$..titles.source..title")[0])
            titles.append(jsonpath.jsonpath(v,"$..titles.item..title")[0])


            abstract = jsonpath.jsonpath(v,"$..abstract..abstract")
            if abstract != False:
                abstracts.append(jsonpath.jsonpath(v,"$..abstract..abstract")[0])
            else:
                abstracts.append("None")

            doi =  jsonpath.jsonpath(v,"$..doi")
            if doi != False:
                dois.append(jsonpath.jsonpath(v,"$..doi")[0])
            else:
                dois.append("None")

            wos_ids.append(jsonpath.jsonpath(v,"$..colluid")[0])
            pubyears.append(jsonpath.jsonpath(v,"$..pub_info..pubyear")[0])


    content = {}
    for i,(doi, wos_id,journal,title, pubyear,abstract) in enumerate(zip(dois, wos_ids, journals,titles, pubyears, abstracts)):
        content[f"{i+1}"] = {
            "doi":doi,
            "wos_id":wos_id,
            "journal":journal,
            "title":title,
            "pubyear":pubyear,
            "abstract":abstract,
        }
    dataInfo[query] = {
        "numberOfItems":numberOfItems,
        "content":content
    }

    with open("../results/2.1 paperDetails_WOS_article_1.json","w") as fp:
        fp.write(json.dumps(dataInfo))
