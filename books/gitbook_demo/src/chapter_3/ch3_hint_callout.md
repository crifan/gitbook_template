# 提示`hint`和插图编号`callout`

## `hint` == `callout` == 提示/警告/错误

演示用插件`callouts`实现的`callout`==`hint`，即各种类型的提示/提醒的效果

语法：

```markdown
> #### {type}:: Your Title
>
> Content
```

其中`{type}`是下面中的任意一种：

* primary
* success
* danger
* warning
* info

> 如果你用过`Bootstrap`就能看出来，其实这几种标题类型就是`Bootstrap`中的标题的类型

效果如下的显示：

### 提示=`tip`=`note`=`info`

> #### info::提醒类信息的标题
> **提醒类信息**中的`内容`

### 成功=`success`= ☑️

> #### success:: 成功的标题
> **成功**中的`内容`

### 警告=`warning`=⚠️

> #### warning::警告的标题
> **警告**中的`内容`

### 错误=`error`=`danger`=❌

> #### danger::错误的标题
> **错误**中的`内容`

### 其他几种(*不常见的*)类型

> #### Tag::`Tag`的标题
> **Tag**中的`内容`

---

> #### Note::`Note`的标题
> **Note**中的`内容`

---

> #### Comment::`Comment`的标题
> **Comment**中的`内容`

---

> #### Hint::`Hint`的标题
> **Hint**中的`内容`

---

> #### Caution::`Caution`的标题
> **Caution**中的`内容`

---

> #### Quote::`Quote`的标题
> **Caution**中的`内容`
