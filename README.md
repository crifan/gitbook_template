# Gitbook模板

最后更新：`v20190529`

## 项目代码仓库

[https://github.com/crifan/gitbook_template](https://github.com/crifan/gitbook_template) 

## 项目作用

1. 用于演示，如何使用`crifan`的`gitbook`的**模板**
2. 别人和自己，可以基于此模板，方便和快速的创建出自己的`gitbook`

此项目主要包括：

* `工具`：主要是自己写的`Makefile`，用于自动化`gitbook`的`初始化`、`调试`、`编译`、`提交`、`部署`等一系列过程
* `gitbook`的demo源码：写了个gitbook的demo的源码，供参考使用，用于创建一个自己的gitbook

## 为何会有这个模板？

主要是之前自己用`Gitbook`创建了很多个`book`，然后就有了把共同部分提取出来的需求，以避免，一旦公共部分改动，就要手动的去更改每个`book`的相关文件，比如`book.json`，`Makefile`，`README.md`。

详见：

* [【已解决】提取Gitbook中Makefile公共部分](http://www.crifan.com/gitbook_extract_common_part_of_makefile)
* [【已解决】gitbook中book.json中能否把公共部分提取出来](http://www.crifan.com/gitbook_extract_book_json_common_part)
* [【基本解决】Makefile中从独立文件比如json中读取配置变量](http://www.crifan.com/makefile_import_read_config_variable_from_file_like_json)

## 使用步骤

下面详细介绍，如何使用本`Gitbook`模板，去创建一个自己的`book`

### 下载模板源码

`git clone https://github.com/crifan/gitbook_template.git`

### 初始化安装`Gitbook`插件

```bash
cd gitbook_template/gitbook_demo/
make init
```

**作用**：内部会调用`gitbook install`去安装插件到`book`下的`node_modules`文件夹中。

插件安装后效果如图：

![Gitbook的install插件到node_modules](img/gitbook_installed_plugin_node_modules.png)

### 调试+编写`book`源码

```bash
make debug
```

**作用**：内部会调用`gitbook serve`去调试，把调试生成的文件都放到`debug`文件夹中。

> **注意**
> 偶尔会出现这个错误：
> `Error: ENOENT: no such file or directory, stat '/Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo/debug/gitbook/gitbook-plugin-copy-code-button/toggle.js'`
> 解决办法是：忽略不用管，再次`make debug`即可。

然后就可以去用浏览器去打开：

[http://localhost:4000/](http://localhost:4000/)

看到此`gitbook`模板demo的效果了：

![Gitbook的debug的localhost效果](img/gitbook_debug_localhost.png)

![Gitbook的各种hint/callout提示的效果](img/gitbook_various_hint_callout_effect.png)

然后就可以去用编辑器，比如`VSCode`，去编辑，更新自己的`markdown`的源码，即`md`文件了。

### 生成静态文件：`html`,`pdf`,`epub`,`mobi`

```bash
make all
```

**作用**：内部会分别调用

* `gitbook build`：生成**静态**`html`
* `gitbook pdf`：生成`pdf`文件
* `gitbook epub`：生成`epub`文件
* `gitbook mobi`：生成`mobi`文件

生成的文件都保存到了`output`文件夹中：

![gitbook生成各种文件到output文件夹中](img/gitbook_generated_all_files_to_ouput_folder.png)

### 提交`commit`+部署`deploy`

当`book`编写完毕，则可以去提交（git源码）并部署（把生成的`html`、`pdf`、`mobi`等文件上传）到自己的服务器上了

```bash
make deploy
```

其中：`deploy` = `upload` + `commit`

**注意**：`deploy`之前，需要修改相关信息为你自己的配置：

#### 对于`commit`

修改`GitbookCommon.mk`中的`github`本地文件路径：

```make
GITHUB_IO_PATH=/Users/crifan/dev/dev_root/github/github.io/crifan.github.io
```

#### 对于`deploy`

* `服务器账号`+`服务器密码`+`服务器IP`+`文件上传路径`：修改`DeployServerInfo.mk`中的配置：

```make
DEPLOY_SERVER_IP=change_to_your_server_ip
DEPLOY_SERVER_USER=change_to_your_server_user
DEPLOY_SERVER_PASSWORD=change_to_your_server_password
DEPLOY_SERVER_PATH=change_to_your_server_path
```

比如我的是：

```make
DEPLOY_SERVER_IP=149.28.136.189
DEPLOY_SERVER_USER=root
DEPLOY_SERVER_PASSWORD=xxxxxx
DEPLOY_SERVER_PATH=/data/wwwroot/book.crifan.com/books
```

##### DEPLOY_SERVER_PASSWORD如包含特殊字符需要转义

如果你的密码`DEPLOY_SERVER_PASSWORD`中包含特殊字符，比如：

* 左括号：`)`
* 井号：`#`
* 问号：`?`

等，需要用反斜杠去`\`转义，比如：

`DEPLOY_SERVER_PASSWORD=xxx)xx#xx?x`

需要写成：

`DEPLOY_SERVER_PASSWORD=xxx\)xx\#xx\?x`

## 其他说明

### 想要部署时忽略多个book中的某个book

如果你和我一样（实际上很少人会有这种）有个特殊需求，有多个book，想要在`make deploy`时，忽略某个book，则可以去：

和`GitbookCommon.mk`同级目录中新建`deploy_ignore_book_list.txt`，然后加上要忽略部署上传的book，比如：

```bash
scientific_network_summary

```

### 此处的`book.json`是合并生成的

此处的`gitbook_demo`的`gibtook`的`book.json`，是通过`Makefile`中的`generate_book_json`调用`python`文件`generateBookJson.py`去从`book_common.json`和`gitbook_demo/book_current.json`去生成的。

而此处，无需自己去单独生成，因为相关的命令，比如：

* `make init`
* `make debug`
* `make all`

会自动（依赖）调用`generate_book_json`去生成`book.json`的。

当然，如果自己想要单独去生成`book.json`，也可以自己调用

`make generate_book_json`

即可。

### 此处的`REAMDME.md`是合并生成的

此处的`README.md`是通过`Makefile`中的`generate_readme_md`调用`../generateReadmeMd.py`去从自己的`README_current.json`加上模板`README_template.md`去生成的。

而此处，无需自己去单独生成，因为相关的命令，比如：

* `make init`
* `make debug`
* `make all`

内部会自动（依赖）调用`generate_readme_md`去生成`README.md`的。

当然，如果自己想要单独去生成`README.md`，也可以自己调用

`make generate_readme_md`

### `make clean_all`

任何时候，都可以用`make clean_all`去清除生成的`book.json`、`output`文件夹中的`html`、`pdf`、`epub`、`mobi`

```bash
➜  gitbook_demo git:(master) ✗ make clean_all
--------------------------------------------------------------------------------
Author  : crifan.com
Version : 20180615
Function: Auto use gitbook to generated files: website/pdf/epub/mobi; upload to remote server; commit to github io repo
		Run 'make help' to see usage
--------------------------------------------------------------------------------
CURRENT_DIR=/Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo
BOOK_NAME=gitbook_demo
rm -f book.json
rm -rf /Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo/output/gitbook_demo/website
rm -rf /Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo/output/gitbook_demo/pdf
rm -rf /Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo/output/gitbook_demo/epub
rm -rf /Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/gitbook_demo/output/gitbook_demo/mobi
```

### `make help`

如果还有其他对于`Makefile`的疑问，可以输入`make help`去查看结果

```bash
➜  gitbook_demo git:(master) ✗ make help
--------------------------------------------------------------------------------
Author  : crifan.com
Version : 20190528
Function: Auto use gitbook to generated files: website/pdf/epub/mobi; upload to remote server; commit to github io repo
                Run 'make help' to see usage
--------------------------------------------------------------------------------
CURRENT_DIR=/Users/crifan/dev/dev_root/gitbook/gitbook_src_root/gitbook_demo
BOOK_NAME=gitbook_demo
NOT found gitbook_demo in IGNORE_FILE_CONTENT=scientific_network_summary

Usage:
  make <target>

Defaul Target: deploy

Targets:
  debug_include             Debug include file
  debug_dir                 Print current directory related info
  debug_python              Debug for makefile call python
  create_folder_debug       Create folder for gitbook local debug
  create_folder_website     Create folder for gitbook website
  create_folder_pdf         Create folder for pdf
  create_folder_epub        Create folder for epub
  create_folder_mobi        Create folder for mobi
  create_folder_all         Create folder for all: website/pdf/epub/mobi
  clean_generated_readme_md Clean generated README.md file
  clean_generated_book_json Clean generated book.json file
  clean_debug               Clean gitbook debug
  clean_website             Clean generated gitbook website whole folder
  clean_pdf                 Clean generated PDF file and whole folder
  clean_epub                Clean generated ePub file and whole folder
  clean_mobi                Clean generated Mobi file and whole folder
  clean_all                 Clean all generated files
  generate_readme_md        Generate README.md from ../README_template.md and README_current.json
  copy_readme               copy README.md to ./src
  copy_gitignore            copy common .gitignore
  generate_book_json        Generate book.json from ../book_common.json and book_current.json
  sync_content              sync content
  init                      gitbook init to install plugins
  install                   gitbook install plugins
  debug                     Debug gitbook
  website                   Generate gitbook website
  pdf                       Generate PDF file
  epub                      Generate ePub file
  mobi                      Generate Mobi file
  all                       Generate all files: website/pdf/epub/mobi
  upload                    Upload all genereted website/pdf/epub/mobi files to remote server using rsync. Create DeployServerInfo.mk which contain deploy server IP+User+Password+Path before use this
  commit                    Commit generated files to github io
  deploy                    Deploy = upload and commit for generated files
  help                      Show help
```
