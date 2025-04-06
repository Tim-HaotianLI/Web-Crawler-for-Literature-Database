# 以下内容的设置在：File->Editor->File and Code Templates->python script

# -*- coding = utf-8 -*-
# @time : 2023/10/9 22:27
# @Author : 
# @File : 2.2 ELSEVIERParseData.py
# @Software : PyCharm

import json
import jsonpath
import re

dataInfo = {}

if __name__ == "__main__":
    pattern = r"\d{4}"

    with open("../results/2.2 infolist_Elsevier_article_1.json","r") as fp:
        infoDict = json.loads(fp.read())

    q = '( "computer vision" OR "machine vision" OR "vision*" OR "visual *" ) AND ( "construction*" OR "infrastructure*" OR "civil engineering" )'

    query = f"TITLE-ABS-KEY({q}) AND PUBYEAR > 1922 AND PUBYEAR < 2024 AND SRCTYPE(J) AND SUBJAREA(ENGI) AND DOCTYPE(AR) AND LANGUAGE(English)"
    numberOfItems = None
    dois = []
    journals = []
    titles = []
    abstracts = []
    pubyears = []
    authkeywords = []

    for i,(k,v) in enumerate(infoDict.items()):
        if i == 0:
            numberOfItems = v
        else:
            try:
                journal = jsonpath.jsonpath(v,"$..prism:publicationName")[0]
                journals.append(journal)
            except:
                journals.append("None")
            titles.append(jsonpath.jsonpath(v,"$..dc:title")[0])
            pubyears.append(re.findall(pattern,jsonpath.jsonpath(v,"$..prism:coverDate")[0])[0])
            try:
                abs = jsonpath.jsonpath(v,"$..dc:description")[0]
                abstracts.append(abs)
            except:
                abstracts.append("None")

            doi = jsonpath.jsonpath(v, "$..prism:doi")
            if doi != False:
                dois.append(jsonpath.jsonpath(v, "$..prism:doi")[0])
            else:
                dois.append("None")
            authkeyword = jsonpath.jsonpath(v,"$..authkeywords")
            if authkeyword != False:
                authkeywords.append(jsonpath.jsonpath(v, "$..authkeywords")[0])
            else:
                authkeywords.append("None")


    content = {}
    for i,(doi, journal, title, pubyear, abstract, keywordstr) in enumerate(zip(dois,journals,titles,pubyears,abstracts,authkeywords)):
        if keywordstr != "None":
            keywords = keywordstr.split(" | ")
        else:
            keywords = "None"

        content[f"{i + 1}"] = {
            "doi": doi,
            "journal":journal,
            "title": title,
            "pubyear":pubyear,
            "abstract": abstract,
            "keywords":keywords
        }

    dataInfo["data"] = {
        "query":query,
        "numberOfItems": numberOfItems,
        "content": content
    }


    with open("../results/2.2 paperDetails_ELSEVIER_article_withKWs.json","w") as fp:
        fp.write(json.dumps(dataInfo))

