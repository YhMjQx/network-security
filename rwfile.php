<?php

/**
 * 文件读写的步骤：
 * 1.打开文件 fopen
 * 2.读写文件 fgets（按行读取），fgetc（按字符读取），fwrite（写文件）
 * 3.关闭文件 fclose
 * 附加函数：
 * 判断文件是否已经达到末尾 feof($fp)
 * 一次性读取文件所有内容 file_get_counts($filename)
 * 使用 file_get_counts 发送GET请求
 * 一次性写入数据到文件中 file_put_counts
 */

/**写文件 */
$wfp = fopen("D:/desktop/rwfile.txt","w");
fwrite($wfp,"ymqyyds\n再坚持两年\n年薪三十万等着你");
fclose($wfp);

/**读文件 */
$rfp = fopen("D:/desktop/rwfile.txt","r");
while(!feof($rfp)) {
    $content = fgets($rfp);
    // $content = str_replace("\n","<br>",$content);  
    // html 页面默认编码格式为utf-8，windows文本默认编码格式为GBK
    // 使用str_replace函数将换行符 \n 替换为 html页面的换行符 <br>，并重新赋值给$content
    echo $content."<br>";  //当然，也可以在输出的同时每一行后面输出 <br>
}
fclose($rfp);

/**使用 file_get_counts 一次性读取整份文件内容 */
$content = file_get_contents("D:/desktop/rwfile.txt");
// $content = iconv("GBK","UTF-8", $content);  
// 想用这个把文件的编码格式转成浏览器的编码格式防止输出乱码呢，没想到竟然报错，而且就算不使用中文输出依旧是对的
// echo $content;
// $content = str_replace("\n","<br>",$content); // 替换换行符，实现换行输出
echo $content."<br>";

/**将文件内容拆分为数组 */
$rows = explode("\n",$content);
print_r($rows);
echo "<br>";

foreach($rows as $row) {
    print_r($row);
    echo "<br>";
}

/**使用 file_get_counts 发送 GET请求 */
// $result = file_get_contents("https://www.bilibili.com/");
// echo $result;  //这个结果就是一个大概的哔站页面，类似于网页爬虫
// //那么是否也可以通过这种方式下载文件或图片到本地呢？
// $photo = file_get_contents("https://i1.hdslb.com/bfs/face/a8280b717cf8d97cd9fdd7fd291c55d0bd5583d5.jpg@240w_240h_1c_1s_!web-avatar-nav.avif");
// //获取到的图片是一个二进制文件，该如何处理
// echo $photo;

/**一次性写入数据到文件中 file_put_counts */
$content = "\n十年以后，一位叫做杨明强的成功人士带领其家乡成为了全国第一网络安全基地\n";
file_put_contents("D:/desktop/rwfile.txt",$content,FILE_APPEND);
// 一定要加上 FILE_APPEND 参数确保是以追加的方式进行写入

/**读取一个csv文件（逗号分隔符），并解析为二维数组
 * 如果一个csv文件存储了用户名和密码，那么我们就可以使用这种方法进行爆破
 */
$content1 = file_get_contents("D:\desktop\\t_teacher.csv");
$content2 = file_get_contents("D:\desktop\\t_student.csv");
$content = explode("\n",$content2);

// 循环之间先定义一个数组，便于存储
$list = array();
for($i = 1;$i<count($content);++$i) {
    $temp = explode(",",$content[$i]);
    array_push($list,$temp);
}
foreach($list as $row) {
    print_r($row);
    echo "<br>";

}

/**实现 文件实时查看 功能
 * ftell($fp) 记录上一次文件指针停留位置（下标）
 * fseek($fp,$pos) 将该文件指针设置为 $pos 
 */

$pos = 0;
while(true) {
    $fp = fopen("D:\desktop\\rwfile.txt","r");
    fseek($fp,$pos);
    while($line = fgets($fp)) {
        $line = mb_substr($line,1);
        // $line = iconv("GBK","UTF-8",$line);

        echo $line."<br>";
    }
    $pos = ftell($fp); 
    //这句话不能放在上面的while循环中，因为第一次循环会将内容输出完，此时$pos已经是文件末尾了
    // 此时 $line = fgets($fp) 赋值便会失败，则从第二次循环开始就会失败
    fclose($fp);


    ob_flush();
    flush();
    sleep(2);
}

?>