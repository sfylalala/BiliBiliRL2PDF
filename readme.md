# BilibiliRL2PDF

## 简介
本项目旨在爬取Bilibili的图文专栏内容，并将其保存为PDF文件。

## 使用步骤

1. 克隆此项目到本地
```
git clone ***
```

2. 安装python依赖
```
    pip install selenium, beautifulsoup4, requests, pdfkit
```
3. 安装Chrome与ChromeDriver
+ 下载并安装Chrome
+ 选择合适的ChromeDriver并下载：https://googlechromelabs.github.io/chrome-for-testing/

    下载完成后，将ChromeDriver解压并放置到一个已加入系统PATH环境变量的目录中

4. 安装wkhtmltopdf（暂不需要）

## 使用方式
1. 配置ChromeDriver路径
    修改代码中的 chrome_driver_path 变量，设置为您的 ChromeDriver 文件的路径。
2. 设置你要爬取的专栏ID
    修改代码中的 rl_id 变量，设置为您想要爬取的Bilibili图文专栏的ID。
3. 执行程序
    ```
    python rl2html.py
    ```
4. 用浏览器打开保存的html文件
    + 使用浏览器的打印功能将其转换为PDF文件.