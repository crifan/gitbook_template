#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Crifan Li
Update: 20200915
Function: Sync README_current.json content to book_current.json
Note: should run this python file from single gitbook foler
      eg: /Users/crifan/dev/dev_root/gitbook/gitbook_src_root/books/gitbook_demo
"""

import os
import json
import codecs
from pprint import pprint

################################################################################
# Global Config
################################################################################

ReadmeCurrentJsonFilename = "README_current.json"
BookCurrentJsonFilename = "book_current.json"

################################################################################
# Internal Function
################################################################################

def loadJsonFromFile(fullFilename, fileEncoding="utf-8"):
    """load and parse json dict from file"""
    with codecs.open(fullFilename, 'r', encoding=fileEncoding) as jsonFp:
        jsonDict = json.load(jsonFp)
        # logging.debug("Complete load json from %s", fullFilename)
        return jsonDict

def saveJsonToFile(jsonDict, fullFilename, indent=2, fileEncoding="utf-8"):
    """
      save dict json into file
      for non-ascii string, output encoded string, without \\uxxxx
    """
    with codecs.open(fullFilename, 'w', encoding="utf-8") as outputFp:
        json.dump(jsonDict, outputFp, indent=indent, ensure_ascii=False)

################################################################################
# Main Part
################################################################################

readmeCurrentJson = {}
bookCurrentJson = {}

# run python in :
currPath = os.getcwd()
# print("currPath=%s" % currPath)
curDirname = os.path.dirname(currPath)
# print("curDirname=%s" % curDirname) # /Users/crifan/dev/dev_root/gitbook/gitbook_src_root/books
curBasename = os.path.basename(currPath)
# print("curBasename=%s" % curBasename) # gitbook_demo
GitbookSrcRootBooks = curDirname
# print("GitbookSrcRootBooks=%s" % GitbookSrcRootBooks)
GitbookSrcRoot = os.path.abspath(os.path.join(GitbookSrcRootBooks, ".."))
# print("GitbookSrcRoot=%s" % GitbookSrcRoot)

CurrentBookPath = currPath
# print("CurrentBookPath=%s" % CurrentBookPath)

CurrentGitbookName = curBasename
# print("CurrentGitbookName=%s" % CurrentGitbookName)
# youdao_note_summary
# gitbook_demo

readmeCurrentJsonFullPath = os.path.join(CurrentBookPath, ReadmeCurrentJsonFilename)
# print("readmeCurrentJsonFullPath=%s" % readmeCurrentJsonFullPath)
readmeCurrentJson = loadJsonFromFile(readmeCurrentJsonFullPath)

bookCurrentJsonFullPath = os.path.join(CurrentBookPath, BookCurrentJsonFilename)
# print("bookCurrentJsonFullPath=%s" % bookCurrentJsonFullPath)
bookCurrentJson = loadJsonFromFile(bookCurrentJsonFullPath)

# pprint("/"*80)
# pprint(readmeCurrentJson)
# pprint("/"*80)
# pprint(bookCurrentJson)

gitRepoName = readmeCurrentJson["gitRepoName"]
# print("gitRepoName=%s" % gitRepoName)
bookName = readmeCurrentJson["bookName"]
# print("bookName=%s" % bookName)
bookDescription = readmeCurrentJson["bookDescription"]
# print("bookDescription=%s" % bookDescription)

bookCurrentJson["title"] = bookName
bookCurrentJson["description"] = bookDescription
pluginsConfig = bookCurrentJson["pluginsConfig"]
# print("pluginsConfig=%s" % pluginsConfig)
pluginsConfig["github-buttons"]["buttons"][0]["repo"] = gitRepoName

PrefixTemplate = "https://book.crifan.com/gitbook/%s/website/"
newPrefix = PrefixTemplate % gitRepoName
# print("newPrefix=%s" % newPrefix)
pluginsConfig["sitemap-general"]["prefix"] = newPrefix
UrlTemplate = "http://book.crifan.com/books/%s/pdf/%s.pdf"
newUrl = UrlTemplate % (gitRepoName, gitRepoName)
# print("newUrl=%s" % newUrl)
pluginsConfig["toolbar-button"]["url"] = newUrl

# print("Updated %s:" % BookCurrentJsonFilename)
# pprint(bookCurrentJson)
saveJsonToFile(bookCurrentJson, bookCurrentJsonFullPath)
