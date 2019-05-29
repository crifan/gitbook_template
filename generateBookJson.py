#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Crifan Li
Version: v1.0 20180615
Function: Generate Gitbook's book.json from ../book_common.json and book_current.json
Note: should run this python file from single gitbook foler
      eg: /Users/crifan/GitBook/Library/Import/youdao_note_summary
"""

import os
import json
from pprint import pprint
import sys
import copy
import codecs
# from collections import OrderedDict

################################################################################
# Global Config
################################################################################

BookJsonTemplateFilename = "book_common.json"
BookJsonCurrentFilename = "book_current.json"
BookJsonOutputFilename = "book.json"

################################################################################
# Internal Function
################################################################################


def recursiveMergeDict(aDict, bDict):
    """
    Recursively merge dict a to b, return merged dict b
    Note: Sub dict and sub list's won't be overwritten but also updated/merged

    example:
(1) input and output example:
input:
{
  "keyStr": "strValueA",
  "keyInt": 1,
  "keyBool": true,
  "keyList": [
    {
      "index0Item1": "index0Item1",
      "index0Item2": "index0Item2"
    },
    {
      "index1Item1": "index1Item1"
    },
    {
      "index2Item1": "index2Item1"
    }
  ]
}

and

{
  "keyStr": "strValueB",
  "keyInt": 2,
  "keyList": [
    {
      "index0Item1": "index0Item1_b"
    },
    {
      "index1Item1": "index1Item1_b"
    }
  ]
}

output:

{
  "keyStr": "strValueB", 
  "keyBool": true, 
  "keyInt": 2,
  "keyList": [
    {
      "index0Item1": "index0Item1_b", 
      "index0Item2": "index0Item2"
    }, 
    {
      "index1Item1": "index1Item1_b"
    }, 
    {
      "index2Item1": "index2Item1"
    }
  ]
}

(2) code usage example:
import copy
cDict = recursiveMergeDict(aDict, copy.deepcopy(bDict))

Note:
bDict should use deepcopy, otherwise will be altered after call this function !!!

    """
    aDictItems = None
    if (sys.version_info[0] == 2): # is python 2
      aDictItems = aDict.iteritems()
    else: # is python 3
      aDictItems = aDict.items()

    for aKey, aValue in aDictItems:
      # print("------ [%s]=%s" % (aKey, aValue))
      if aKey not in bDict:
        bDict[aKey] = aValue
      else:
        bValue = bDict[aKey]
        # print("aValue=%s" % aValue)
        # print("bValue=%s" % bValue)
        if isinstance(aValue, dict):
          recursiveMergeDict(aValue, bValue)
        elif isinstance(aValue, list):
          aValueListLen = len(aValue)
          bValueListLen = len(bValue)
          bValueListMaxIdx = bValueListLen - 1
          for aListIdx in range(aValueListLen):
            # print("---[%d]" % aListIdx)
            aListItem = aValue[aListIdx]
            # print("aListItem=%s" % aListItem)
            if aListIdx <= bValueListMaxIdx:
              bListItem = bValue[aListIdx]
              # print("bListItem=%s" % bListItem)
              recursiveMergeDict(aListItem, bListItem)
            else:
              # print("bDict=%s" % bDict)
              # print("aKey=%s" % aKey)
              # print("aListItem=%s" % aListItem)
              bDict[aKey].append(aListItem)

    return bDict


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

templateJson = {}
currentJson = {}

# run python in :
# /Users/crifan/GitBook/Library/Import/youdao_note_summary
# /Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo
currPath = os.getcwd()
# print("currPath=%s" % currPath)
curDirname = os.path.dirname(currPath)
# print("curDirname=%s" % curDirname)
curBasename = os.path.basename(currPath)
# print("curBasename=%s" % curBasename)
BookRootPath = curDirname
CurrentGitbookName = curBasename
print("BookRootPath=%s" % BookRootPath)
# /Users/crifan/GitBook/Library/Import
# /Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template
print("CurrentGitbookName=%s" % CurrentGitbookName)
# youdao_note_summary
# gitbook_demo

bookJsonTemplateFullPath = os.path.join(BookRootPath, BookJsonTemplateFilename)
# print("bookJsonTemplateFullPath=%s" % bookJsonTemplateFullPath)
# /Users/crifan/GitBook/Library/Import/book_common.json
with open(bookJsonTemplateFullPath) as templateJsonFp:
    templateJson = json.load(templateJsonFp, encoding="utf-8")
    # templateJson = json.load(templateJsonFp, encoding="utf-8", object_pairs_hook=OrderedDict)
    # templateJson = OrderedDict(templateJson)
    # print("type(templateJson)=%s" % (type(templateJson))) #type(templateJson)=<class 'collections.OrderedDict'>

bookJsonCurrentFullPath = os.path.join(BookRootPath, CurrentGitbookName, BookJsonCurrentFilename)
# print("bookJsonCurrentFullPath=%s" % bookJsonCurrentFullPath)
with open(bookJsonCurrentFullPath) as currentJsonFp:
    currentJson = json.load(currentJsonFp, encoding="utf-8")
    # currentJson = json.load(currentJsonFp, encoding="utf-8", object_pairs_hook=OrderedDict)
    # currentJson = OrderedDict(currentJson)

# pprint("/"*80)
# pprint(templateJson)
# pprint("/"*80)
# pprint(currentJson)

# pprint("/"*80)
bookJson = recursiveMergeDict(templateJson, copy.deepcopy(currentJson))

# pprint("-a"*40)
# pprint(templateJson)
# pprint("-b"*40)
# pprint(currentJson)
# pprint("-c"*40)
# pprint(bookJson)
# print("type(templateJson)=%s" % (type(templateJson)))
# print("type(currentJson)=%s" % (type(currentJson)))
# print("type(bookJson)=%s" % (type(bookJson)))

bookJsonFullPath = os.path.join(BookRootPath, CurrentGitbookName, BookJsonOutputFilename)
# print("bookJsonFullPath=%s" % bookJsonFullPath)
saveJsonToFile(bookJson, bookJsonFullPath)