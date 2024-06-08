from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pdfkit
import requests

# 设置ChromeDriver路径
chrome_driver_path = 'C:\Program Files\Google\Chrome\chromedriver.exe'  # 替换为你的chromedriver路径

def init_chrome():
    # 初始化Chrome浏览器
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式，不打开浏览器界面
    options.add_argument('--disable-gpu')

    # 启动浏览器
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_h1_and_cv_id_list(rl_id):
    url = f"https://api.bilibili.com/x/article/list/web/articles?id={rl_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.bilibili.com/',
    }
    print(url)
    response = requests.get(url, headers=headers)
    data = response.json()
    h1 = data['data']['list']['name']
    articles = data['data']['articles']
    cv_id_list = [article['id'] for article in articles]
    print(cv_id_list)
    print(h1)
    return h1, cv_id_list


# 通过cv_id获取文章内容并生成PDF文件
def cv_id_to_html(cv_id, driver):
    cv_url = f"https://www.bilibili.com/read/cv{cv_id}"
    
    driver.get(cv_url)

    # 等待页面加载完成，假设我们等待文章内容的div加载完成
    try:
        # 使用显式等待来等待特定元素加载完成
        content_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'article-content'))
        )
        # 获取页面内容
        page_source = driver.page_source

        # 解析页面内容
        soup = BeautifulSoup(page_source, 'html.parser')
        article_content = soup.find('div', id='article-content')

        if article_content:
            # 找到原文中的 <h1> 标签并替换为 <h2> 标签
            original_h1 = soup.find('h1', class_='title')
            if original_h1:
                h2 = soup.new_tag('h2')
                h2.string = original_h1.get_text()

            # 找到所有 <figure> 标签并替换为 <img> 标签
            figures = article_content.find_all('figure')
            for figure in figures:
                img = figure.find('img')
                if img and 'data-src' in img.attrs:
                    # 构建新的 img 标签
                    new_img_tag = soup.new_tag('img', src='https:' + img['data-src'], width=img.get('width'), height=img.get('height'))
                    # 替换 <figure> 标签为新的 img 标签
                    figure.replace_with(new_img_tag)

            # 获取 <div id="read-article-holder" class="normal-article-holder read-article-holder"> 内部的内容
            content_holder = article_content.find('div', class_='normal-article-holder read-article-holder')

            if content_holder:
                # 获取内容并移除容器 div 标签
                final_content = ''.join(str(element) for element in content_holder.contents)
                if original_h1:
                    final_content = str(h2) + final_content
                print(final_content)
                # save to file
                # with open(f"cv{cv_id}.html", "w", encoding="utf-8") as file:
                #     file.write(final_content)
                # print(f"cv{cv_id}.html 文件已生成")
            return final_content

        else:
            print("Article content not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


# 主函数：获取所有文章并合并为一个HTML文件
def main(rl_id):
    driver = init_chrome()
    h1, cv_id_list = get_h1_and_cv_id_list(rl_id)
    all_articles_content = ""

    for cv_id in cv_id_list:
        article_content = cv_id_to_html(cv_id, driver)
        all_articles_content += article_content + "\n"

    driver.quit()

    # 添加 HTML 文档结构
    final_html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>合并的文章</title>
        <style>
            body {{
                font-family: 'SimSun', Arial, sans-serif;
            }}
        </style>
    </head>
    <body>
        <h1>{h1}</h1>
        {all_articles_content}
    </body>
    </html>
    """

    final_html_name = f"{rl_id}.html"
    # 将合并后的内容保存到HTML文件
    with open(final_html_name, "w", encoding="utf-8") as file:
        file.write(final_html_content)
    
    print("合并的HTML文件已生成：", final_html_name)

# 示例调用
rl_id = 587988
# get_h1_and_cv_id_list(rl_id)
main(rl_id)

# cv_id = 17594139
# driver = init_chrome()
# cv_id_to_html(cv_id, driver)