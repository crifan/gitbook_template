# 代码高亮显示

此处`gitbook`中**代码高亮**的插件用的是`prism`

官网是：[http://prismjs.com](http://prismjs.com)

下面列出常见的几种代码的代码高亮效果。

## `markdown`

```markdown
# HTTP简介

`HTTP`=`Hyper Text Transfer Protocol`=`超文本传输协议`

HTTP的总体思路是：

* 客户端：向服务器发送一个`请求`=`Request`，请求头包含请求的方法、URI、协议版本、以及包含请求修饰符、客户信息和内容的类似于MIME的消息结构。
* `服务器`：以一个状态行作出`响应`=`Response`，相应的内容包括消息协议的版本，成功或者错误编码加上包含服务器信息、实体元信息以及可能的实体内容。

简而言之就是一个你问我答的协议：
* 客户端Client 问=`请求`=`Request`
* 服务器Server 答=`响应`=`Response`

关于HTTP的相关的详细知识，或许很多人不是很熟悉。
但是：
- 作为普通电脑用户的你，经常用`浏览器`（`IE`/`Chrome`/`Firefox`等）去浏览网页时
- 作为程序开发，用网络库去调用服务器后台提供的接口时
其实内部都用到了HTTP的技术。

```

## `python`

```python
def saveJsonToFile(jsonDict, fullFilename, indent=2, fileEncoding="utf-8"):
  """
    save dict json into file
    for non-ascii string, output encoded string, without \uxxxx
  """
  with codecs.open(fullFilename, 'w', encoding="utf-8") as outputFp:
      json.dump(jsonDict, outputFp, indent=indent, ensure_ascii=False)

################################################################################
# Main Part
################################################################################

templateJson = {}
currentJson = {}

# run python in : /Users/crifan/GitBook/Library/Import/youdao_note_summary
currPath = os.getcwd()
curBasename = os.path.basename(currPath)
CurrentGitbookName = curBasename
print("CurrentGitbookName=%s" % CurrentGitbookName) #youdao_note_summary

bookJsonTemplateFullPath = os.path.join(BookRootPath, BookJsonTemplateFilename)
# print("bookJsonTemplateFullPath=%s" % bookJsonTemplateFullPath)
# /Users/crifan/GitBook/Library/Import/book_common.json
with open(bookJsonTemplateFullPath) as templateJsonFp:
    templateJson = json.load(templateJsonFp, encoding="utf-8")
```

## `javascript`

```js
// extract single sub string from full string
// eg: extract '012345678912345' from 'www.ucows.cn/qr?id=012345678912345'
export function  extractSingleStr(curStr, pattern, flags='i') {
  let extractedStr = null;

  let rePattern = new RegExp(pattern, flags);
  console.log(rePattern);

  let matches = rePattern.exec(curStr);
  console.log(matches);

  if (matches) {
    extractedStr = matches[0];
    console.log(extractedStr);
  }

  if (extractedStr === null) {
    extractedStr = "";
  }

  console.log(`curStr=${curStr}, pattern=${pattern}, flags=${flags} -> extractedStr=${extractedStr}`);

  return extractedStr;
}

```

## `html`

```html

<!DOCTYPE HTML>
<html lang="zh-hans" >
    <head>
        <meta charset="UTF-8">
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <title>HTTP相关 · HTTP知识总结</title>
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="description" content="">
        <meta name="generator" content="GitBook 3.2.3">
        <meta name="author" content="Crifan Li <admin@crifan.com>">

        <link rel="stylesheet" href="../gitbook/style.css">
        <link rel="stylesheet" href="../gitbook/gitbook-plugin-search-plus/search.css">
```

## `css`

```css

a#weixin {
  position: relative;
}

#weixin img {
  visibility: hidden;
  opacity: 0;
  transform: translate(0, 10px);
  transition: all 0.3s ease-in-out;
  position: absolute;
  right: -30px;
  bottom: 40px;
  width: 150px;
  height: 150px;
}

#weixin:hover img {
  visibility: visible;
  transform: translate(0, 0px);
  opacity: 1;
}
```
