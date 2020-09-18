#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Crifan Li
Update: 20200918
Function: Update crifan.github.io README.md
Note: should run this python file from single gitbook foler
      eg: /Users/crifan/dev/dev_root/gitbook/gitbook_src_root/books/gitbook_demo
"""

from datetime import datetime,timedelta
import os
import codecs
import json
import argparse
import re

################################################################################
# Global Config
################################################################################

ReadmeMdFilename = "README.md"
ReadmeCurrentJsonFilename = "README_current.json"

################################################################################
# Internal Function
################################################################################

def datetimeToStr(inputDatetime, format="%Y%m%d_%H%M%S"):
    """Convert datetime to string

    Args:
        inputDatetime (datetime): datetime value
    Returns:
        str
    Raises:
    Examples:
        datetime.datetime(2020, 4, 21, 15, 44, 13, 2000) -> '20200421_154413'
    """
    datetimeStr = inputDatetime.strftime(format=format)
    # print("inputDatetime=%s -> datetimeStr=%s" % (inputDatetime, datetimeStr)) # 2020-04-21 15:08:59.787623
    return datetimeStr

def getCurDatetimeStr(outputFormat="%Y%m%d_%H%M%S"):
    """
    get current datetime then format to string

    eg:
        20171111_220722

    :param outputFormat: datetime output format
    :return: current datetime formatted string
    """
    curDatetime = datetime.now() # 2017-11-11 22:07:22.705101
    # curDatetimeStr = curDatetime.strftime(format=outputFormat) #'20171111_220722'
    curDatetimeStr = datetimeToStr(curDatetime, format=outputFormat)
    return curDatetimeStr

def loadTextFromFile(fullFilename, fileEncoding="utf-8"):
    """load file text content from file"""
    with codecs.open(fullFilename, 'r', encoding=fileEncoding) as fp:
        allText = fp.read()
        # logging.debug("Complete load text from %s", fullFilename)
        return allText

def loadJsonFromFile(fullFilename, fileEncoding="utf-8"):
    """load and parse json dict from file"""
    with codecs.open(fullFilename, 'r', encoding=fileEncoding) as jsonFp:
        jsonDict = json.load(jsonFp)
        # logging.debug("Complete load json from %s", fullFilename)
        return jsonDict

def saveTextToFile(fullFilename, text, fileEncoding="utf-8"):
    """save text content into file"""
    with codecs.open(fullFilename, 'w', encoding=fileEncoding) as fp:
        fp.write(text)
        fp.close()

################################################################################
# Main Part
################################################################################
parser = argparse.ArgumentParser(description='Update crifan.github.io README.md')
parser.add_argument('--curBookRepoName', type=str, help='current gitbook repo name, eg: mobile_network_evolution_history')
# parser.add_argument('--curBookTitle', type=str, help='current gitbook title, eg: 移动网络演化史')
parser.add_argument('--localGithubIoPath', type=str, help='local github.io path')

args = parser.parse_args()
# print("args=%s" % args)
curBookRepoName = args.curBookRepoName
print("curBookRepoName=%s" % curBookRepoName)
localGithubIoPath = args.localGithubIoPath
print("localGithubIoPath=%s" % localGithubIoPath)

readmeMdFullPath = os.path.join(localGithubIoPath, ReadmeMdFilename)
# print("readmeMdFullPath=%s" % readmeMdFullPath)
curReadmeMdStr = loadTextFromFile(readmeMdFullPath)
# print("curReadmeMdStr=%s" % curReadmeMdStr)

curDatetimeStr = getCurDatetimeStr("%Y%m%d")
# print("curDatetimeStr=%s" % curDatetimeStr)
newLastUpdateStr = "最后更新：`%s`" % curDatetimeStr
print("newLastUpdateStr=%s" % newLastUpdateStr)
newReamdMdStr = re.sub("最后更新：`(\d+)`", newLastUpdateStr, curReadmeMdStr)
# print("newReamdMdStr=%s" % newReamdMdStr)

foundGitbookList = re.search("\* 现有哪些电子书\s(?P<curGitbookListMd>.+)\* 其他独立内容", newReamdMdStr, re.DOTALL)
# print("foundGitbookList=%s" % foundGitbookList)
if foundGitbookList:
  curGitbookListMd = foundGitbookList.group("curGitbookListMd")
  # print("curGitbookListMd=%s" % curGitbookListMd)
  allBookMatchList = re.finditer("\[(?P<bookTitle>[^]]+)\]\(https://crifan\.github\.io/(?P<bookRepoName>\w+)/website\)", curGitbookListMd)
  # print("allBookMatchList=%s" % allBookMatchList)
  curBookDict = {}
  for curIdx, eachBookMatch in enumerate(allBookMatchList):
    # print("eachBookMatch=%s" % eachBookMatch)
    # print("%s %s %s" % ("-"*10, curIdx, "-"*10))
    bookTitle = eachBookMatch.group("bookTitle")
    # print("bookTitle=%s" % bookTitle)
    bookRepoName = eachBookMatch.group("bookRepoName")
    # print("bookRepoName=%s" % bookRepoName)
    curBookDict[bookRepoName] = bookTitle

  # print("curBookDict=%s" % curBookDict)
  if curBookRepoName in curBookDict.keys():
    print("%s already in current readme -> no need add, do nothing" % curBookRepoName)
  else:
    print("%s not in current readme -> need add it" % curBookRepoName)
    currPath = os.getcwd()
    # print("currPath=%s" % currPath)
    readmeCurrentJsonFullPath = os.path.join(currPath, ReadmeCurrentJsonFilename)
    # print("readmeCurrentJsonFullPath=%s" % readmeCurrentJsonFullPath)
    readmeCurrentJson = loadJsonFromFile(readmeCurrentJsonFullPath)
    # print("readmeCurrentJson=%s" % readmeCurrentJson)
    curBookTitle = readmeCurrentJson["bookName"]
    # print("curBookTitle=%s" % curBookTitle)
    curBookDict[curBookRepoName] = curBookTitle
    # print("updated curBookDict=%s" % curBookDict)
    # generate new gitbook list md
    newSingleBookMdList = []
    for eachBookReoName, eachBookTitle in curBookDict.items():
      singleBookMd = "    * [%s](https://crifan.github.io/%s/website)" % (eachBookTitle, eachBookReoName)
      # print("singleBookMd=%s" % singleBookMd)
      newSingleBookMdList.append(singleBookMd)
    # print("newSingleBookMdList=%s" % newSingleBookMdList)
    newGitbookListMd = "\n".join(newSingleBookMdList)
    # print("newGitbookListMd=%s" % newGitbookListMd)
    newGitbookListMd += "\n"
    newReamdMdStr = newReamdMdStr.replace(curGitbookListMd, newGitbookListMd)
    print("newReamdMdStr=%s" % newReamdMdStr)

saveTextToFile(readmeMdFullPath, newReamdMdStr)
print("Updated %s" % readmeMdFullPath)
