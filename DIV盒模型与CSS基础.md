[TOC]



# ==DIV盒模型与CSS基础==

## 一、CSS的使用方法

要为HTML元素设定样式，有以下三种方式来使用CSS：

### 1.在元素中指定 style 属性

```css
<td style="border: solid 2px red; background-color: white; font-size: 20px"></td>
```

> 也称为内嵌样式，只针对对应的标签生效

### 2.在页面中嵌入 style 样式块

```css
<style>
    td {
        background-color: #7fffd4;  /* 颜色的RGB编码 */
        width: 25px;
        text-align: center;  /*设置文本位置处于中央*/
        font-size: 30px;
    }
</style>
```

> 通常建议将style标签放置于head标签中，针对当前页面所有元素生效

### 3.在页面中引入外部CSS文件

```css
<link rel="stylesheet" type="text/css" href="/page/css/bootstrap.css" />
```

> 外部CSS文件，可以针对全站的引入了这个CSS的多个页面生效，放置于head标签中

## 二、CSS选择器

选择器是指CSS如何与元素及样式建立关联关系的一种很重要的手段。CSS选择器的使用，决定了CSS样式作用于哪一个元素或哪一种元素，对于快速或精准设置元素的样式将至关重要，CSS样式主要分为以下6类：

### 1.标签选择器

使用类型选择器，可以在这种元素类型的每个实例上应用声明

```css
/* 为当前页面中的所有单元格设置统一样式 */
td {
    background-color: #7fffd4;
    width: 25%;
    text-align: center;
    font-size:30px;
}
```

### 2.类选择器

通过设置元素的class属性定位元素，在同一个页面中，多个元素可以归属为同一个类

```css
/* 类选择器以 . 开头，对于在元素的标签中指定了 class="title" 的元素设计如下样式 */
.title {
    color: white;  /*文字的颜色*/
    font-size: 20px;  /*文字大小*/
    float: left;  /*设置元素向左靠动*/
    margin-right: 10px;  /*设置元素距离右边10px*/
}
```

### 3.ID选择器

HTML页面的任何一个元素，即任何一个标签，都拥有ID这个属性，我们可以通过为元素设置一个唯一的ID识别符，进而利用CSS的ID选择器对其设计样式

```css
/* ID选择器，以 # 开头，对于在元素标签中指定了 id="title" 的元素设计样式 */
#title {
    color: white;
    font-size: 20px;
    float: right;
    magrin-right: 10px;
}

```

### 5.组合选择器

可以将**标签选择器、ID选择器、类选择器和属性选择器等**，组合成不同的选择器类型来构成更复杂的选择器。通过组合选择器可以更加精确地处理被希望赋予某种样式的元素。我们也可以通过指定父子关系来对元素进行选择

> 这种话听不懂，大白话就是：对某个大类下面的某一个小类中的元素设计样式。不多说，看代码

```css
/* 组合使用 ID 和 标签 选择器，并实现了层次关系 */
/* id为button时，对具有该属性的所有td的单元格设计样式 */
#button td {
    font-size: 20px;
    font-family: 微软雅黑;
    text-align: center;
}
```



### 4.属性选择器

```css
/* 为div标签元素下拥有 type="button" 属性的元素设计样式 */
div [type="button"] {
    color: white;
    font-size: 20px;
}
```



### 6.伪类选择器

设计 伪类和伪元素 可以实现一些页面中的**动态效果**。使用伪类可以根据一些情况改变文档中连接的样式，如根据链接是否被访问，何时被访问以及用户和文档的交互方式来应用改变。借助于伪元素，可以更改元素的第一个字母和第一行的样式，或者添加源文档中没有出现过的元素。

```css
/* 使用 hover 伪类设置鼠标划过时的变换效果 */
#button td:hover {
    background-color: red;  /* 当鼠标滑动时，变换背景颜色 */
}
```



## 三、DIV盒模型

### 1.盒模型（Box Model）

盒模型（也可以称之为盒子模型）是CSS中一个重要的概念，理解了盒模型才能更好地排版。我们来想象一下一个盒子，它有：外边距（margin，与其他盒子之间的距离）、边框（border）、内间距（padding，盒子边框与内容之间的填充距离）、内容（content）四个属性

让我们俯视这个盒子，它有上下左右四条边，所以每个属性都包括四个部分：上下左右；这四个部分可以同时设置，也可以分别设置

内间距可以理解为，盒子里装的东西与边框之间的距离，而边框有厚薄和颜色之分，内容就是盒子中间装的东西，外边距就是边框外面自动留出的一段空白

我们换种方式来理解这个盒模型：

- 内容（content）就是盒子里装的东西，可多可少，可以使任意类型
- 填充（padding）就是怕盒子里装的东西损坏，而添加的泡沫或其他抗震的辅料
- 边框（border）就是盒子本身了，当然，边框也是有厚薄和颜色的
- 边界（margin）则说明盒子摆放的时候不能能全部堆在一起，要留出一定的空隙保持通风，同时也方便取出

![image-20240204224314087](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240204224314087.png)

> 在线代页面中，通常使用DIV+CSS进行布局设计，而table主要用于展示二维表格数据，不再用于布局
