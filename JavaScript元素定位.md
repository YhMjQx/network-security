[TOC]



# ==JavaScript元素定位==

## 利用JavaScript实现计算器

### 一、DOM操作

JavaScript直接操作页面的元素的方法合集，称为DOM（Document Object Model），实际上就是页面当中利用JavaScript操作页面元素的方法的集合。是一套js代码接口，另外还有一套BOM（Browser Object Model），用于通过JS直接操作浏览器，比如前进，后退，历史，导航，刷新等。

```html
    <!-- 下面是js代码 -->
    <!-- 获取一个元素（定位，选择） -->
    <!-- 定义一个变量，使用 var 标记，在这里给他赋值为计算器的标题，innerHTML表示为该元素的值 -->
    <!-- 被函数体包裹的代码，如果没有触发条件或调用，则代码不会被执行 -->
    <script type="text/javascript">
        
        function alertclactitle() {
        // 在函数体中，变量之前加 var ，表示是当前函数内部的局部变量，如果不加则会被视为全局变量
        // 建议在函数体中都加上，否则会导致变量生命周期混乱
            var calctitle = document.getElementById("calc-title").innerHTML;
            window.alert(calctitle);
        }

        // JS中通过其他方式来获取元素
        // document.getElementsByClassName("point");   //获取到三个class=point的元素
        // document.getElementsByName("result");  //获取到name=result的1个元素
        // document.getElementsByTagName("div");  //获取到所有标签为div的元素
        // JS中也可以通过XPath来定义
    </script>
</head>
<body onload="alertclactitle()">
    <!-- onload 元素事件，页面加载完成之后则自动执行 -->
    <div id="top">
        <div class="point red"></div>
        <div class="point green"></div>
        <div class="point blue"></div>
        <div id="calc-title">DIV版蜗牛计算器</DIV></div>
    </div>

    <div id="result-out" name="result">
        <div id="result-in">

        </div>
    </div>
    
    <div id="button">
        <!-- onclick 当前元素被单机时，调用alertclactitle() 这个函数 -->
        <div onclick="alertclactitle()">AC</div>
```

**值的注意的是，一般情况下，我们需要将js代码包裹成函数，否则也会造成代码执行混乱，最终无法达到我们想要的结果。**就拿着一段代码来说，如果我蒙了没有将js代码包裹成函数，而是直接写，那么就会先执行js代码，然后再渲染元素，但是既然元素都没有渲染，js又从何去寻找我们想要的数据呢

解决办法：

#### 方法一：就如同上面的方法一样，将js代码包裹成函数

此时函数其实和C语言中的意思差不多，调用方式也差不多。都是在内存中有一块地址，调用时就是利用该地址寻找

#### 方法二：将js代码放在元素渲染之后

```html
<body>
    <div id="top">
        <div class="point red"></div>
        <div class="point green"></div>
        <div class="point blue"></div>
        <div id="calc-title">DIV版蜗牛计算器</DIV></div>
    </div>

    <div id="result-out" name="result">
        <div id="result-in">

        </div>
    </div>
    
    <div id="button">
        <div>AC</div>
        
<script type="text/javascript">
    var calctitle = document.getElementById("calc-title").innerHTML;
    window.alert(calctitle);
</script>
```

#### JS的元素定位

```js
// getElementById 为单数，通过此函数最终的返回结果就是该元素本身
document.getElementById("calc-title").innerHTML;

document.getElementsByClassName("point");   //获取到三个class=point的元素。此时getElementsByClassName是复数，最终的返回结果是一个数组

document.getElementsByName("result");  //获取到name=result的1个元素。此时getElementsByName是复数，最终的返回结果是一个数组。此时就需要使用数组的下标来获取元素

document.getElementsByTagName("div");  //获取到所有标签为div的元素。此时getElementsByTagName是复数，最终的返回结果是一个数组。此时就需要使用数组的下标来获取元素




document.getElementsByTagName("div")[0];  //就表示该返回数组的第一个元素
document.getElementsByTagName("div")[0].innerHTML;  //就表示该返回数组的第一个元素所包含的值
```

##### XPath

```
JS也可以通过XPath来定义
XML：可扩展标记语言（extension Markup Language）。用于描述一组数据，标记可以自己任意定义，类似于数据库当中的行和列
HTML：超文本标记语言，用于描述页面元素，所有标记都是实现约定好的（W3C组织），浏览器厂商统一支持
```

比如下面用XML描述了两本书

```xml
<bookstore>
	<book id="1001">
    	<title>Harry Potter</title>
        <author>] K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>
    <book id="1002">
    	<title>Harry Potter</title>
        <author>] K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>
</bookstore>
```

就类似于这么个布局

![image-20240205215823258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240205215823258.png)

以下XPATH的示例说明

```js
var result = document.evaluate("//a[@href]", document, nul1, xpathResult.ANY_TYPE, nu11);
//   //a[@href]  表示当前页面中所有的超链接（标签为 a ），具有href属性的元素

nodes=document.evaluate("//div[@id='xxx']", document).iterateNext();
//   //div[@id='xxx']  表示当前页面中，所有标签为div的元素中，id='xxx'的元素
```

