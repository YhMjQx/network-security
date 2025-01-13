package com.ymqyyds.vul;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class RCE {
    // Java 执行命令的手段 Runtime ProcessBuilder
    public void useRuntime() throws Exception{
        // 首先是 Runtime
        // 没有回显的情况
//        Runtime r = Runtime.getRuntime();
//        r.exec("calc.exe");

        // 有回显的情况  需要定义一个 InputStream 对象来接收回显内容，然后使用 InputStreamReader 对象来对 InputStream 对象内容的读取，然后再用缓冲区实现对内容的读取
        Runtime r = Runtime.getRuntime();
        InputStream is = r.exec("whoami /user").getInputStream();
        InputStreamReader reader = new InputStreamReader(is,"GBK");
        BufferedReader bufferedReader = new BufferedReader(reader);
        String line = "";
        // 按行读取，按行输出
        while((line = bufferedReader.readLine()) != null) {
            System.out.println(line);
        }
        is.close();
        reader.close();
        bufferedReader.close();
    }

    public void useProcessBuilder() throws Exception{
        //接下来是 ProcessBuilder

        // 没有回显的情况
//        ProcessBuilder processBuilder = new ProcessBuilder("ipconfig");
//        processBuilder.start();

        // 有回显的情况s
        ProcessBuilder processBuilder = new ProcessBuilder("whoami","/user");
        InputStream is = processBuilder.start().getInputStream();
        InputStreamReader reader = new InputStreamReader(is,"GBK");
        BufferedReader bufferedReader = new BufferedReader(reader);
        String line = "";
        while ((line = bufferedReader.readLine()) != null) {
            System.out.println(line);
        }
        is.close();
        reader.close();
        bufferedReader.close();
    }

    public static void main(String[] args) throws Exception{
        RCE rce = new RCE();
        rce.useRuntime();
        rce.useProcessBuilder();
    }
}
