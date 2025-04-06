# Web Crawler for Different Literature Database

[TOC]

## Project Introduction

This project contains three different crawler codes for three different literature databases: Web of Science, Scopus, and ASCE Library. In addition, the project includes parsing programs for the crawler results. See the table below for details information:

| Literature Database | Crawler Code                              | mechanism  | Parsing Code                                                 |
| ------------------- | ----------------------------------------- | ---------- | ------------------------------------------------------------ |
| Web of Science      | `./1. codes_getData/1.1 WOSQuery.py`      | selenium   | `./1. codes_getData/1.2 WOSParseData.py` <br>`./1. codes_getData/1.3 getmetadata_WOS.py` |
| Scopus              | `./1. codes_getData/2.1 ELSEVIERQuery.py` | Scopus API | `./1. codes_getData/2.2 ELSEVIERParseData.py`                |
| ASCE Library        | `./1. codes_getData/3.1 ASCEQuery.py`     | selenium   | `./1. codes_getData/3.2 getmetadata_ASCE.py`                 |

## Result

The crawling and parsing results of each Literature Database can be checked in the following files:

**Web of Science**: `./results/paperDetails_WOS_withKWs.json`

**Scopus**: `./results/paperDetails_ELSEVIER.json`

**ASCE Library**: `./results/paperDetails_ASCE_withKWs.json`

These three results were combined together by the following code: `./1. codes_getData/4. ItemCombination.py`; 

The combined results see here: `./results/combinedResults.json`