#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Function: Generate gitbook markdown files from entry md file SUMMARY.md. if md existed, update md file time.
Author: Crifan Li
Update: 20210524
"""

import argparse
import os
import re
from datetime import datetime
import random

argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--md-file", type=str, required=True, help="full path of entry SUMMARY.md file")
argParser.add_argument("--disable-update-existed-md", action='store_true', help="disable update existed md file modification time")
argParser.add_argument("--disable-random-time", action='store_true', help="disable use random time for update time")
argParser.add_argument("-r", "--random-range", type=int, default=10*60, help="for random time, the range. in seconds. default 600 = 10 minutes")
args = argParser.parse_args()

# if not args.file:
#     raise Exception("SUMMARY.md file required !")

summaryMdFullPath = args.md_file
# isUpdateMdWhenExist = args.update_existed_md
print("args.disable_update_existed_md=%s" % args.disable_update_existed_md)
isUpdateMdWhenExist = not args.disable_update_existed_md
print("args.disable_random_time=%s" % args.disable_random_time)
isRandomUpdateTime = not args.disable_random_time
randomRange = args.random_range

# # for debug
# summaryMdFullPath = "/Users/limao/dev/crifan/gitbook/gitbook_template/books/linux_usage_dev_summary/src/SUMMARY.md"
# isUpdateMdWhenExist = True
# isRandomUpdateTime = True
# randomRange = 10 * 60 # in seconds

print("summaryMdFullPath=%s" % summaryMdFullPath)
print("isUpdateMdWhenExist=%s" % isUpdateMdWhenExist)
print("isRandomUpdateTime=%s" % isRandomUpdateTime)
print("randomRange=%s" % randomRange)

bookRootPath = os.path.dirname(summaryMdFullPath)
print("bookRootPath=%s" % bookRootPath)

summaryMdLineList = open(summaryMdFullPath).readlines()
# print("summaryMdLineList=%s" % summaryMdLineList)

def updateFileTime(filePath, newAccessTime=None, newModificationTime=None, isAccessSameWithModif=True):
    """Update file access time and modification time

    Args:
        filePath (str): file path
        newAccessTime (int): new file access time, float
        newModificationTime (int): new file modification time, float
        isAccessSameWithModif (bool): make access same with modification 
    Returns:
        None
    Raises:
    Examples:
        newModificationTime=1620549707.664307
    """
    if (not newAccessTime) and (not newModificationTime):
        return
    
    statInfo = os.stat(filePath)
    # print("statInfo=%s" % statInfo)
    # print("statInfo.st_info=%s" % statInfo.st_info)

    if not newAccessTime:
        oldAccessTime = statInfo.st_atime # 1619490904.6651974
        # print("oldAccessTime=%s" % oldAccessTime)
        newAccessTime = oldAccessTime

    if not newModificationTime:
        oldModificationTime = statInfo.st_mtime # 1617002149.62217
        # print("oldModificationTime=%s" % oldModificationTime)
        newModificationTime = oldModificationTime

    if isAccessSameWithModif:
        newAccessTime = newModificationTime

    os.utime(filePath, (newAccessTime, newModificationTime))

summaryMdLineCount = len(summaryMdLineList)
print("Total md line count: %d" % summaryMdLineCount)
for curIdx, eachLine in enumerate(summaryMdLineList):
    curNum = curIdx +1
    print("%s %s %s" % ("-"*20, curNum, "-"*20))
    eachLine = eachLine.strip()
    # print("eachLine=%s" % eachLine)
    # * [Linux系统概述](linux_sys_overview/README.md)
    foundMd = re.search("\*\s+\[(?P<mdName>[^\]]+)\]\((?P<mdPath>[\w/]+\.md)\)", eachLine)
    if foundMd:
        mdName = foundMd.group("mdName")
        mdPath = foundMd.group("mdPath")
        print("mdName=%s, mdPath=%s" % (mdName, mdPath))

        mdAbsPath = os.path.join(bookRootPath, mdPath)

        mdFolderPath = os.path.dirname(mdAbsPath)
        if mdFolderPath:
            os.makedirs(mdFolderPath, exist_ok=True)

        if os.path.exists(mdAbsPath):
            # print("Existed md: %s" % mdAbsPath)
            print("Existed md: %s" % mdPath)
            if isUpdateMdWhenExist:
                curDateTime = datetime.now() # datetime.datetime(2021, 5, 9, 16, 41, 9, 399425)
                curTimestamp = curDateTime.timestamp() # 1620549669.399425
                if isRandomUpdateTime:
                    lessTime = random.randint(0, randomRange) # 13451
                    newModifTime = curTimestamp - lessTime # 1620554635.993749 -> 1620541184.993749
                else:
                    newModifTime = curTimestamp
                updateFileTime(mdAbsPath, newModificationTime=newModifTime)
                # print("Updated modifiy time for md: %s" % mdAbsPath)
                print("Updated modifiy time for md: %s" % mdAbsPath)
        else:
            with open(mdAbsPath, "w") as mdFp:
                titleMdStr = "# %s\n" % mdName
                mdFp.write(titleMdStr)
                # print("Created md: %s" % mdAbsPath)
                print("Created md: %s" % mdPath)
