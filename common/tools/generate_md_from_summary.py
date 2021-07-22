#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Function: Generate gitbook markdown files from entry md file SUMMARY.md. if md existed, update md file time.
Author: Crifan Li
Update: 20210720
"""

import argparse
import os
import re
from datetime import datetime
import random
import subprocess

################################################################################
# Global Varivale
################################################################################

isRandomUpdateTime = None
randomRange = None

################################################################################
# Util Function
################################################################################

def runCommand(consoleCommand):
    """run command using subprocess call"""
    isRunCmdOk = False
    errMsg = "Unknown Error"

    try:
        resultCode = subprocess.check_call(consoleCommand, shell=True)
        if resultCode == 0:
            isRunCmdOk = True
            errMsg = ""
        else:
            isRunCmdOk = False
            errMsg = "%s return code %s" % (consoleCommand, resultCode)
    except subprocess.CalledProcessError as callProcessErr:
        isRunCmdOk = False
        errMsg = str(callProcessErr)
        # "Command 'ffmpeg -y -i /Users/crifan/.../debug/extractAudio/show_112233_video.mp4 -ss 00:00:05.359 -to 00:00:06.763 -b:a 128k /.../show_112233_video_000005359_000006763.mp3 2> /dev/null' returned non-zero exit status 1."

    return isRunCmdOk, errMsg

def getCommandOutput(consoleCommand, consoleOutputEncoding="utf-8", timeout=2):
    """get command output from terminal

    Args:
        consoleCommand (str): console/terminal command string
        consoleOutputEncoding (str): console output encoding, default is utf-8
        timeout (int): wait max timeout for run console command
    Returns:
        console output (str)
    Raises:
    """
    # print("getCommandOutput: consoleCommand=%s" % consoleCommand)
    isRunCmdOk = False
    consoleOutput = ""
    try:
        # consoleOutputByte = subprocess.check_output(consoleCommand)

        consoleOutputByte = subprocess.check_output(consoleCommand, shell=True, timeout=timeout)

        # commandPartList = consoleCommand.split(" ")
        # print("commandPartList=%s" % commandPartList)
        # consoleOutputByte = subprocess.check_output(commandPartList)
        # print("type(consoleOutputByte)=%s" % type(consoleOutputByte)) # <class 'bytes'>
        # print("consoleOutputByte=%s" % consoleOutputByte) # b'640x360\n'

        consoleOutput = consoleOutputByte.decode(consoleOutputEncoding) # '640x360\n'
        consoleOutput = consoleOutput.strip() # '640x360'
        isRunCmdOk = True
    except subprocess.CalledProcessError as callProcessErr:
        cmdErrStr = str(callProcessErr)
        print("Error %s for run command %s" % (cmdErrStr, consoleCommand))

    # print("isRunCmdOk=%s, consoleOutput=%s" % (isRunCmdOk, consoleOutput))
    return isRunCmdOk, consoleOutput

def listSubfolderFiles(subfolder, isContainSubfolder=False):
    """os.listdir recursively

    Args:
        subfolder (str): sub folder path
        isContainSubfolder (bool): whether contain sub folder. Default is False
    Returns:
        list of str
    Raises:
    """
    allSubItemList = []
    curSubItemList = os.listdir(path=subfolder)
    for curSubItem in curSubItemList:
        curSubItemFullPath = os.path.join(subfolder, curSubItem)
        if os.path.isfile(curSubItemFullPath):
            allSubItemList.append(curSubItemFullPath)
        elif os.path.isdir(curSubItemFullPath):
            subSubItemList = listSubfolderFiles(curSubItemFullPath, isContainSubfolder)
            allSubItemList.extend(subSubItemList)

    if isContainSubfolder:
        allSubItemList.append(subfolder)

    return allSubItemList

def updateFileTime(fileOrFolderPath, newAccessTime=None, newModificationTime=None, isAccessSameWithModif=True):
    """Update file access time and modification time

    Args:
        fileOrFolderPath (str): file or folder path
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
    
    statInfo = os.stat(fileOrFolderPath)
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

    os.utime(fileOrFolderPath, (newAccessTime, newModificationTime))

def updateSingleFile(fileOrFolderFullPath, isUpdateFolderForFile=True):
    curDateTime = datetime.now() # datetime.datetime(2021, 5, 9, 16, 41, 9, 399425)
    curTimestamp = curDateTime.timestamp() # 1620549669.399425
    if isRandomUpdateTime:
        lessTime = random.randint(0, randomRange) # 13451
        newModifTime = curTimestamp - lessTime # 1620554635.993749 -> 1620541184.993749
    else:
        newModifTime = curTimestamp
    isFile = os.path.isfile(fileOrFolderFullPath)
    if isUpdateFolderForFile and isFile:
        folderFullPath = os.path.dirname(fileOrFolderFullPath)
        updateFileTime(fileOrFolderFullPath, newModificationTime=newModifTime)
        updateFileTime(folderFullPath, newModificationTime=newModifTime)
        print("Updated modifiy time of file and folder for: %s" % fileOrFolderFullPath)
    else:
        updateFileTime(fileOrFolderFullPath, newModificationTime=newModifTime)
        print("Updated modifiy time for file/folder: %s" % fileOrFolderFullPath)

################################################################################
# Main
################################################################################

argParser = argparse.ArgumentParser()
argParser.add_argument("-m", "--mode", default="auto", choices=["auto", "summary", "git"], help="operation mode. options: auto/summary/git. auto: auto check from input foler or summary.md. folder to use git, summary.md to use summary.")
argParser.add_argument("-e", "--entry", type=str, required=True, help="Entry folder or file. Folder: book root path, eg: /Users/limao/dev/crifan/gitbook/gitbook_template/books/information_security_overview/; File: full path of SUMMARY.md, eg: /Users/limao/dev/crifan/gitbook/gitbook_template/books/information_security_overview/src/SUMMARY.md")
argParser.add_argument("--disable-update-existed-md", action='store_true', help="disable update existed md file modification time")
argParser.add_argument("--disable-random-time", action='store_true', help="disable use random time for update time")
argParser.add_argument("-r", "--random-range", type=int, default=10*60, help="for random time, the range. in seconds. default 600 = 10 minutes")
args = argParser.parse_args()

# if not args.file:
#     raise Exception("SUMMARY.md file required !")

mode = args.mode
entry = args.entry
# isUpdateMdWhenExist = args.update_existed_md
print("args.disable_update_existed_md=%s" % args.disable_update_existed_md)
isUpdateMdWhenExist = not args.disable_update_existed_md
print("args.disable_random_time=%s" % args.disable_random_time)
isRandomUpdateTime = not args.disable_random_time
randomRange = args.random_range

# for debug
# entry = "/Users/limao/dev/crifan/gitbook/gitbook_template/books/linux_usage_dev_summary/src/SUMMARY.md"
# entry = "/Users/limao/dev/crifan/gitbook/gitbook_template/books/android_app_security_crack/"
# entry = "/Users/limao/dev/crifan/gitbook/gitbook_template/books/web_automation_tool_playwright"
# entry = "."
# isUpdateMdWhenExist = True
# isRandomUpdateTime = True
# randomRange = 10 * 60 # in seconds

print("mode=%s" % mode)
print("entry=%s" % entry)
print("isUpdateMdWhenExist=%s" % isUpdateMdWhenExist)
print("isRandomUpdateTime=%s" % isRandomUpdateTime)
print("randomRange=%s" % randomRange)

if mode == "auto":
    if os.path.isdir(entry):
        mode = "git"
    else:
        mode = "summary"
print("mode=%s" % mode)

# # for debug
# entry = "/Users/limao/dev/crifan/gitbook/gitbook_template/books/guard_your_car_safety"

# to support '.', convert to real full path
entry = os.path.abspath(entry)
print("entry=%s" % entry)

if mode == "git":
    bookRootPath = entry
    # /Users/limao/dev/crifan/gitbook/gitbook_template/books/grasp_hacker_track_security_analysis/
    gitStatusCmd = "git status"
    fullGitCmd = "cd %s; %s" % (bookRootPath, gitStatusCmd)
    print("fullGitCmd=%s" % fullGitCmd)
    # cd /Users/limao/dev/crifan/gitbook/gitbook_template/books/information_security_overview/src/; git status
    isCheckCmdRunOk, cmdResult = getCommandOutput(fullGitCmd)
    print("isCheckCmdRunOk=%s, cmdResult=%s" % (isCheckCmdRunOk, cmdResult))
    if isCheckCmdRunOk:
        # extract git status files
        """
        (1) normal
        /Users/limao/dev/crifan/gitbook/gitbook_template/books/information_security_overview/

            Your branch is up to date with 'origin/master'.

            Changes not staged for commit:
            (use "git add/rm <file>..." to update what will be committed)
            (use "git checkout -- <file>..." to discard changes in working directory)

                    modified:   README_current.json
                    modified:   src/SUMMARY.md
                    modified:   src/appendix/reference.md
                    deleted:    src/other_related/tool/capture_package/README.md
                    deleted:    src/other_related/tool/capture_package/wireshark.md
                    modified:   src/security_common/ctf_competition/README.md
                    modified:   src/security_overview/README.md
                    modified:   src/web_security/README.md
                    modified:   src/web_security/common_tools/os/kali_linux.md

            no changes added to commit (use "git add" and/or "git commit -a")

        (2) still not add:
        /Users/limao/dev/crifan/gitbook/gitbook_template/books/grasp_hacker_track_security_analysis/

            On branch master

            No commits yet

            Untracked files:
            (use "git add <file>..." to include in what will be committed)

                    .gitignore
                    Makefile
                    README.md
                    README_current.json
                    book.json
                    book_current.json
                    node_modules
                    src/

            nothing added to commit but untracked files present (use "git add" to track)
        
        (3) contain untracked file

            On branch master
            Your branch is up to date with 'origin/master'.

            Changes not staged for commit:
            (use "git add/rm <file>..." to update what will be committed)
            (use "git checkout -- <file>..." to discard changes in working directory)

                    modified:   README.md
                    modified:   README_current.json
                    modified:   src/README.md
                    modified:   src/SUMMARY.md
                    modified:   src/appendix/reference.md
                    modified:   src/penetration_method/web_frontend/README.md
                    modified:   src/penetration_related/security_analysis/README.md
                    deleted:    src/penetration_related/security_analysis/log.md
                    deleted:    src/penetration_related/security_analysis/network_anlysis_tool.md
                    deleted:    src/penetration_tool/port_scan/nmap.md

            Untracked files:
            (use "git add <file>..." to include in what will be committed)

                    src/assets/img/zenmap_screenshot_detail.png
                    src/assets/img/zenmap_screenshot_host.png
                    src/assets/img/zenmap_screenshot_http.png
                    src/assets/img/zenmap_screenshot_profile_editor.png
                    src/penetration_tool/port_scan/nmap/

            no changes added to commit (use "git add" and/or "git commit -a")
        
        (4)中文输出
            您的分支与上游分支 'origin/master' 一致。

            尚未暂存以备提交的变更：
            （使用 "git add/rm <文件>..." 更新要提交的内容）
            （使用 "git restore <文件>..." 丢弃工作区的改动）
                    修改：     README.md
                    修改：     README_current.json
                    修改：     book.json
                    修改：     book_current.json
                    修改：     src/README.md
                    修改：     src/SUMMARY.md
                    修改：     src/android_background/related_info/apk_file.md
...
                    修改：     src/android_safety_tech/encrypt_overview/harden_method/common_harden_method.md
                    修改：     src/appendix/reference.md

            未跟踪的文件:
            （使用 "git add <文件>..." 以包含要提交的内容）
                    src/android_background/related_info/android_vm/
                    src/android_background/related_info/smali.md
...
                    src/assets/img/jvm_vs_dvm_flow.png

            修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）

        (5)中文输出：新git仓库
             git status
            位于分支 master

            尚无提交

            未跟踪的文件:
            （使用 "git add <文件>..." 以包含要提交的内容）
                    .gitignore
                    Makefile
                    README.md
                    README_current.json
                    book.json
                    book_current.json
                    node_modules
                    src/

            提交为空，但是存在尚未跟踪的文件（使用 "git add" 建立跟踪）
        """
        toUpdatFileDictList = []

        notStagedFileDictList = []

        toUpdateStr = None
        notStagedStr = None
        discardChangeStrEn = "to discard changes in working directory\)"
        discardChangeStrZhcn = "丢弃工作区的改动）"
        untrackFileStrEn = "Untracked files"
        untrackFileStrZhcn = "未跟踪的文件"
        addCommitStrEn = "no changes added to commit"
        addCommitStrZhcn = "修改尚未加入提交"
        # foundNotStagedStr = re.search("to discard changes in working directory\)\s+(?P<notStagedStr>.+?)\s+((Untracked files:)|(no changes added to commit))", cmdResult, flags=re.S)
        # notStagePatternStr = "((%s)|(%s))\)\s+(?P<notStagedStr>.+?)\s+((((%s)|(%s)):)|(((%s)|(%s))))" % (discardChangeStrEn, discardChangeStrZhcn, untrackFileStrEn, untrackFileStrZhcn, addCommitStrEn, addCommitStrZhcn)
        notStagePatternStr = "((%s)|(%s))\s+(?P<notStagedStr>.+?)\s+((((%s)|(%s)):)|(((%s)|(%s))))" % (discardChangeStrEn, discardChangeStrZhcn, untrackFileStrEn, untrackFileStrZhcn, addCommitStrEn, addCommitStrZhcn)
        print("notStagePatternStr=%s" % notStagePatternStr)
        foundNotStagedStr = re.search(notStagePatternStr, cmdResult, flags=re.S)
        if foundNotStagedStr:
            notStagedStr = foundNotStagedStr.group("notStagedStr")
            print("notStagedStr=%s" % notStagedStr)

            notStagedLineList = notStagedStr.splitlines()
            print("notStagedLineList=%s" % notStagedLineList)
            for eachNotStageStr in notStagedLineList:
                modifyStrEn = "modified:"
                modifyStrZhcn = "修改："
                deletedStrEn = "deleted:"
                deletedStrZhcn = "删除："
                # foundFile = re.search("\t(?P<action>(modified)|(deleted)):\s+(?P<filePath>\S+)$", eachNotStageStr)
                actionFilePatternStr = "\t?(?P<action>(((%s)|(%s)))|(((%s)|(%s))))\s+(?P<filePath>\S+)$" % (modifyStrEn, modifyStrZhcn, deletedStrEn, deletedStrZhcn)
                print("actionFilePatternStr=%s" % actionFilePatternStr)
                foundFile = re.search(actionFilePatternStr, eachNotStageStr)
                if foundFile:
                    action = foundFile.group("action") # 'modified'
                    filePath = foundFile.group("filePath") # 'README_current.json'
                    print("action=%s, filePath=%s" % (action, filePath))
                    curFileDict = {
                        "action": action,
                        "filePath": filePath,
                    }
                    notStagedFileDictList.append(curFileDict)
            print("notStagedFileDictList=%s" % notStagedFileDictList)

        toUpdatFileDictList.extend(notStagedFileDictList)

        untrackedStr = None
        untrackedFileDictList = []
        includeCommitedStrEn = "to include in what will be committed\)"
        includeCommitedStrZhcn = "以包含要提交的内容）"
        commitEmptyStrEn = "nothing added to commit but untracked files present"
        commitEmptyStrZhcn = "提交为空，但是存在尚未跟踪的文件"
        # foundUntrackedStr = re.search("to include in what will be committed\)\s+(?P<untrackedStr>.+?)\s+no changes added to commit", cmdResult, flags=re.S)
        untrackedPatternStr = "((%s)|(%s))\s+(?P<untrackedStr>.+?)\s+((%s)|(%s)|(%s)|(%s))" % (includeCommitedStrEn, includeCommitedStrZhcn, addCommitStrEn, addCommitStrZhcn, commitEmptyStrEn , commitEmptyStrZhcn)
        print("untrackedPatternStr=%s" % untrackedPatternStr)
        foundUntrackedStr = re.search(untrackedPatternStr, cmdResult, flags=re.S)
        if foundUntrackedStr:
            untrackedStr = foundUntrackedStr.group("untrackedStr")
            print("untrackedStr=%s" % untrackedStr)

            untrackedLineList = untrackedStr.splitlines()
            print("untrackedLineList=%s" % untrackedLineList)

            for eachUntrackedLine in untrackedLineList:
                # src/assets/img/zenmap_screenshot_detail.png
                # src/penetration_tool/port_scan/nmap/
                # foundUntrackedFile = re.search("\t?(?P<untrackedFile>src/.+)$", eachUntrackedLine)
                foundUntrackedFile = re.search("\t?(?P<untrackedFile>src/.*)$", eachUntrackedLine)
                if foundUntrackedFile:
                    untrackedFile = foundUntrackedFile.group("untrackedFile")
                    print("untrackedFile=%s" % untrackedFile)
                    untrackedFullPath = os.path.join(bookRootPath, untrackedFile)
                    if os.path.isfile(untrackedFullPath):
                        # src/assets/img/zenmap_screenshot_detail.png
                        curUntrackedFileDict = {
                            "action": "added",
                            "filePath": untrackedFullPath,
                        }
                        untrackedFileDictList.append(curUntrackedFileDict)
                    elif os.path.isdir(untrackedFullPath):
                        # list all sub folder files
                        # 'src/penetration_tool/port_scan/nmap/'
                        # Note: following return file and FOLDER, for later support update folder modified time
                        allSubfolderFullPathList = listSubfolderFiles(untrackedFullPath, isContainSubfolder=True)
                        # allSubfolderFullPathList = listSubfolderFiles(untrackedFullPath, isContainSubfolder=False)
                        print("allSubfolderFullPathList=%s" % allSubfolderFullPathList)
                        for eachSubFullPath in allSubfolderFullPathList:
                            print("eachSubFullPath=%s" % eachSubFullPath)
                            subfolderItemDict = {
                                # "action": "added",
                                "action": "added:",
                                "filePath": eachSubFullPath,
                            }
                            untrackedFileDictList.append(subfolderItemDict)

        print("untrackedFileDictList=%s" % untrackedFileDictList)

        toUpdatFileDictList.extend(untrackedFileDictList)
        print("toUpdatFileDictList=%s" % toUpdatFileDictList)

        toUpdateItemCount = len(toUpdatFileDictList)
        print("toUpdateItemCount=%s" % toUpdateItemCount)

        print("Total to update item count: %d" % toUpdateItemCount)

        for curIdx, eachToUpdateDict in enumerate(toUpdatFileDictList):
            curNum = curIdx +1
            print("%s %s %s" % ("-"*20, curNum, "-"*20))
            curAction = eachToUpdateDict["action"]
            curFilePath = eachToUpdateDict["filePath"]
            print("curAction=%s, curFilePath=%s" % (curAction, curFilePath))
            if os.path.isabs(curFilePath):
                curFileFullPath = curFilePath
            else:
                curFileFullPath = os.path.join(bookRootPath, curFilePath)

            # isModified = curAction == "modified"
            # isAdded = curAction == "added"
            # isDeleted = curAction == "deleted"
            isModified = (curAction == "modified:") or (curAction == "修改：")
            isAdded = (curAction == "added:") or (curAction == "新增：")
            isDeleted = (curAction == "deleted") or (curAction == "删除：")

            isNeedUpdate = isModified or isAdded
            isNeedUpdate = not isDeleted

            if isNeedUpdate:
                updateSingleFile(curFileFullPath)
            else:
                print("Not update %s %s" % (curAction, curFilePath))
    else:
        print("! Failed to get output for command: %s" % fullGitCmd)
elif mode == "summary":
    if os.path.isdir(entry):
        # is foler root path, add SUMMARY.md
        SRC_FOLDER = "src"
        SUMMARY_FILE = "SUMMARY.md"
        entry = os.path.join(entry, SRC_FOLDER, SUMMARY_FILE)

    summaryMdFile = entry

    bookSrcPath = os.path.dirname(entry)
    print("bookSrcPath=%s" % bookSrcPath)
    # bookRootPath = os.path.dirname(bookSrcPath)
    # print("bookRootPath=%s" % bookRootPath)

    summaryMdLineList = open(summaryMdFile).readlines()
    # print("summaryMdLineList=%s" % summaryMdLineList)

    summaryMdLineCount = len(summaryMdLineList)

    print("Total to update item count: %d" % summaryMdLineCount)
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

            mdAbsPath = os.path.join(bookSrcPath, mdPath)

            mdFolderPath = os.path.dirname(mdAbsPath)
            if mdFolderPath:
                os.makedirs(mdFolderPath, exist_ok=True)

            if os.path.exists(mdAbsPath):
                # print("Existed md: %s" % mdAbsPath)
                print("Existed md: %s" % mdPath)
                if isUpdateMdWhenExist:
                    updateSingleFile(mdAbsPath)
            else:
                with open(mdAbsPath, "w") as mdFp:
                    titleMdStr = "# %s\n" % mdName
                    mdFp.write(titleMdStr)
                    # print("Created md: %s" % mdAbsPath)
                    print("Created md: %s" % mdPath)
