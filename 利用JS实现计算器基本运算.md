[TOC]



# ==利用JS实现计算器基本运算==

#### 一、基本操作

##### 1.当点击每个按钮时，，需要响应单击事件，并输入相应的值在result元素中显示出来

##### 2.要能够计算结果，并将结果显示出来，那么该如何计算结果呢

##### 3.如何避免连续输入运算符的bug，如何解决连续输入小数点的bug

#### 二、响应单击事件并显示输入的内容

```js
<script>
    function clicknum(num) {
    var result=document.getElementById("result-in");
    result.innerHTML += num;  
    //这里加的是字符串，而不是数字相加。比如第一次num为7，第二次num为8，那么第一次结果为7，第二次结果就为78
    //也可以用 result.innerHTML = result.innerHTML + num; 
}
</script>


<div onclick="clicknum(innerHTML)">7</div>
<div onclick="clicknum(innerHTML)">8</div>
<div onclick="clicknum(innerHTML)">9</div>

<div onclick="clicknum(innerHTML)">4</div>
<div onclick="clicknum(innerHTML)">5</div>
<div onclick="clicknum(innerHTML)">6</div>

<div onclick="clicknum(innerHTML)">1</div>
<div onclick="clicknum(innerHTML)">2</div>
<div onclick="clicknum(innerHTML)">3</div>

<div onclick="clicknum(innerHTML)">0</div>
```

#### 三、响应单击事件，输入运算符

```js
<script>
    //相应单击运算符事件
    function clickoperater(operator) {
        var option = document.getElementById("result-in");
        option.innerHTML += operator;
    }

</script>


<div onclick="clickoperater('%')">%</div>
<div onclick="clickoperater('/')">÷</div>
<div onclick="clickoperater('*')">*</div>
<div onclick="clickoperater('-')">-</div>
<div onclick="clickoperater('+')">+</div>

```

#### 四、如何运算result中表达式的结果

```js
</script>
    //计算结果，使用 eval 函数，该函数可将字符串作为代码执行
    function getresult() {
        var result = document.getElementById("result-in");
        result.innerHTML=eval(result.innerHTML);
    }
</script>

<div onclick="getresult()">=</div>
```

#### 五、解决运算符连续输入的问题

##### 方法一：

设置一个开关，使用 布尔（true/false或0/1...） 类型的值，在<script>级中定义一个全局变量，在function级别操作，进行判断

```js
 <script>
    var isOperatorHasClicked = false;  //判断是否刚点击了操作符 + - * /
    var isGotResult = false;  //判断是否刚点击了 =
    //响应单击数字事件
    function clickNum(num) {
        var result=document.getElementById("result-in"); //这里我是为了获得id="result-			in"的元素，然后再利用下面的代码让元素中的内容为我所传的参数
        result.innerHTML += num;

        // result.innerHTML 的返回类型是字符串
        //这里加的是字符串，而不是数字相加。比如第一次num为7，第二次num为8，那么第一次结果为7，第二			次结果就为78
        //也可以用 result.innerHTML = result.innerHTML + num; 
        isOperatorHasClicked = false;  //点击了数字，说明上一次点击的并不是操作符，故修改 该值		为false

        //有一个bug，我们有可能点击了数字、操作符、数字之后再点击退格键，此时							isOperatorHasClicked = false，那么再点击操作符就有导致了两个操作符同时存在
    }
    //相应单击运算符事件
    function clickOperator(operator) {
        var result = document.getElementById("result-in");
        if (isOperatorHasClicked == false) {
            result.innerHTML += operator;
            isOperatorHasClicked = true;  //点击了操作符之后说明需要修改该值为true
            isGotResult = false;  //并且此时表示运算并没有结束，故还没有得到结果，于是该值需要设				置为false
        }

    }
    // //如果上一次点击的不是操作符，那么此时就说明需要显示新点击的操作符并表示操作符已被点击（isOperatorHasClicked = true），还没有得到结果（isGotResult = false）
    // //如果已经点击过操作符再次点击操作符时，就需要删掉原来的操作符，替换为新点击的操作符
    // else if (isOperatorHasClicked == true) {
    //     backSpace();
    //     result.innerHTML += operator;
    // }

    //计算结果，使用 eval 函数，该函数可将字符串作为代码执行
    function getResult() {
        var result = document.getElementById("result-in");
        result.innerHTML=eval(result.innerHTML);
        isGotResult = true;   //当点击了 = 之后就说明得到了结果，此时该值设为true
    }

    //清空结果
    //注意函数名不要直接用clear关键字，否则会无响应
    function clearResult() {
        // result = document.getElementById("result-in");
        // result.innerHTML="";
        document.getElementById("result-in").innerHTML="";
        isOperatorHasClicked = false;
    }

    //删除最后一位字符
    function backSpace() {
        var result = document.getElementById("result-in");
        //  上面这行代码表示返回的是了整个元素，此时做的任何修改都会体现在元素本身
        //  如果var result = document.getElementById("result-in").innerHTML  则表示			result是一个字符串，在这个函数当中，只是一个临时变量，无法做到对元素本身的修改
        var len = result.innerHTML.length;  //取字符串长度
        result.innerHTML = result.innerHTML.substr(0,len-1);
    }
</script>
```

该方法需要定义全局变量，同时需要在各个函数中不断重置开关的值，导致函数与函数之间耦合度太高，相互之间影响过大，任何一个函数体出问题，就会导致所有结果出问题，出现各个错误。较不建议。

##### 方法二：

判断最后一个字符是否是运算符，如果是+-*/ 运算符中的一个，则再输入运算符时，直接替换而不是连接

```js
function clickOperator(operator) {
    var result = document.getElementById("result-in");
    var len=result.innerHTML.length;
    var lastchar=result.innerHTML[len-1];  //找到字符串的最后一个字符，判断最后一个字符是否为操作符
    if (lastchar == '+' || lastchar == '-' || lastchar == '*' || lastchar == '/' || lastchar == '%') {
        result.innerHTML = result.innerHTML.substr(0,len-1) + operator;
        //如果是，就拿掉最后一个新的字符串，并用新点击的操作符替换掉
    }
    else {
        result.innerHTML += operator;
         //如果最后一个字符不是操作符，则正常连接即可
    }
}
```

本方案，没有与其他函数或全局变量进行耦合，都是在一个函数体中进行的，较为建议。高内聚，低耦合。

#### 六、解决小数点连续输入的问题

首先，小数点不能直接调用 clickOperator() 和 clickNum() 这俩函数，会导致耦合增加，用该另起一个函数，clickPoint() 。

```js
//点击小数点
function clickPoint(point) {
    var result = document.getElementById("result-in");
    var len=result.innerHTML.length;
    var lastchar=result.innerHTML[len-1];
    //为防止小数点重复输入的问题，判断最后一个字符是否为小数点
    if (lastchar == '.' ) {
        //如果是，则直接退出，不允许输入
        exit ;
    }
    else {
        //如果不是，则再正常加上小数点
        result.innerHTML += point;
    }
}

<div onclick="clickPoint('.')">.</div>

```

#### 七、解决得出结果之后点击小数点，小数点还会跟在结果后面的问题

按照windows自带的计算器来看，得出结果后再点击小数点，会直接重置为 '0.' 

```js
//点击小数点
function clickPoint(point) {
    var result = document.getElementById("result-in");
    var len=result.innerHTML.length;
    var lastchar=result.innerHTML[len-1];
    if (lastchar == '.' ) {
        exit ;
    }
    else {
        result.innerHTML += point;
    }

    //为解决得出结果后点击小数点，小数点会跟在结果后的问题。先判断刚刚是不是得出了结果
    if (isGotResult == true) {
        //如果是，则清空结果栏，并重置显示为 0.
        result.innerHTML="";
        result.innerHTML += '0'+ point;
        isGotResult = false;
    }

}
```





#### 八、解决点击等于号之后再次输入数字，新数字会连接原来的结果的问题

```js
 var isGotResult = false; 

//响应单击数字事件
function clickNum(num) {
    var result=document.getElementById("result-in"); //这里我是为了获得id="result-in"的元素，然后再利用下面的代码让元素中的内容为我所传的参数

    // result.innerHTML 的返回类型是字符串
    //这里加的是字符串，而不是数字相加。比如第一次num为7，第二次num为8，那么第一次结果为7，第二次结果就为78
    //也可以用 result.innerHTML = result.innerHTML + num; 
    
    //首先利用一个大的if，判断前面的数字是否为之前通过 = 得到的值
    if (isGotResult == false) {
        //如果不是，就正常连接数字
        result.innerHTML += num;
    }
    else {
        //如果是，此时再点击数字应该先清空原来的结果，再单独显示新的数字
        //但是我们还要考虑一种情况，如果是得出了结果，又点击了操作符，那么此时应该也是直接连接新的数字
        //所以需要先判断，目前最后一个字符是否为操作符
        var result = document.getElementById("result-in");
        var len=result.innerHTML.length;
        var lastchar=result.innerHTML[len-1];
        if (lastchar == '+' || lastchar == '-' || lastchar == '*' || lastchar == '/' || lastchar == '%') {
            //如果最后一个字符是操作符，那么就直接连接新的数字，并重置 isGotResult = false
            result.innerHTML += num;
            isGotResult = false;
        }
        else {
            //如果最后一个字符不是操作符，那么就清空结果栏，并单独显示新的数字，并重置isGotResult = false
            result.innerHTML="";
            result.innerHTML += num;
            isGotResult = false;
        }
    }
}

//计算结果，使用 eval 函数，该函数可将字符串作为代码执行
function getResult() {
    var result = document.getElementById("result-in");
    result.innerHTML=eval(result.innerHTML);
    isGotResult = true;
}
```

#### 九、解决正负号替换操作

```js
<script>
    function getReverse() {
        var result = document.getElementById("result-in");
        result.innerHTML = eval('0' - result.innerHTML);
}
</script>
```

