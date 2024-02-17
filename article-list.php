<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript" src="../jquery-3.4.1.min.js"></script>
    <title>ymqyydss</title>
    <style>
        table {
            margin: auto;
            text-align: center;
            border: solid 2px greenyellow;
            width: 1000px;
        }
        td {
            border: solid 1px blue;
            height: 30px;
            /* border-spacing: 0px; */
        }

        button {
            border: solid 1px blue;
            height: 30px;
            /* float: right; */
        }

    </style>

    <script>
        function doPop($articleid) {
            // window.alert($articleid);
        
            var result = window.confirm("确定删除改文章吗？");
            // window.confirm();  函数会弹窗给出确定和取消两个选项，点击确定返回true
            if (result != true) {
                window.alert("取消删除");
                return false;
            }

            $.post("articlePop.php","articleid="+$articleid,function(data){
                if(data == "delete-pass") {
                    window.alert("删除成功");
                    location.reload(); // 刷新此页面
                    // location.href="article-list.php";  // 重新跳转到自己的页面，相当于刷新
                }
                else {
                    window.alert("删除失败"+data);
                }
            });

    }
    </script>
</head>
<body>

    <table>
        <tr>
            <td>articleid</td>
            <td>headline</td>
            <td>updatetime</td>
            <td>function</td>
        </tr>

        <?php

        $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote') or die("数据库连接失败");
        mysqli_set_charset($conn,'utf8');

        $sql = "select articleid , headline , updatetime from article";
        $result = mysqli_query($conn,$sql);

        //将数据库查询的 结果集 中的数据取出，保存到一个数组中
        $rows = mysqli_fetch_all($result);
        // print_r($rows);  最终的数组是一个二维数组，联想数据库中的表，
        // 二维数组第一个元素就是第一行，第一行的第一个元素就是 articleid

        //foreach中 每一个$row 都是$rows的一个元素，所以每一个$row就是一行数据
        // 遍历结果集数据并输出到页面中
        // foreach($rows as $row) {
        //     echo $row[0]." ~ ".$row[1]." ~ ".$row[2]."<br>";
        // }


        // 遍历结果集数据并在表格中展示
        // 我们观察结果一共有三列，分别是 articleid , headline , updatetime
        // 行数会由foreach自动执行

        // 我么可以使用整体的表格代替下面的分开输出
        // echo '<table>';
        // echo '<tr>';
        // echo '<td>articleid</td>';
        // echo '<td>headline</td>';
        // echo '<td>updatetime</td>';
        // echo  '</tr>';

        foreach($rows as $row) {
            echo '<tr>';
            echo '<td>'.$row[0].'</td>';
            echo '<td><a href="read-article.php?id='.$row[0].'">'.$row[1].'</a></td>';
            echo '<td>'.$row[2].'</td>';
            echo '<td><button onclick="doPop('.$row[0].')">删 除</button></td>';
            echo  '</tr>';
        }

        //输出完结果关闭数据库
        mysqli_close($conn);

        ?>

    </table>
    
</body>
</html>
