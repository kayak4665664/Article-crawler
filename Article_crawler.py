import requests
import re
import bs4
import os
import sys

urls = {}
urls_path = os.path.split(os.path.realpath(sys.argv[0]))[0] + "\\" + "urls.txt"
url_str = "源地址"
keywords = []
keywords_path = os.path.split(os.path.realpath(sys.argv[0]))[
    0] + "\\" + "keywords.txt"
keyword_str = "关键词"
search_by_keywords = False


def add_url(url_name):
    tmp_url = input("URL：")
    urls[url_name] = tmp_url


def remove_url(url_name):
    del urls[url_name]


def clean_all_urls():
    del urls
    print("\n已清空！\n")


def add_keyword(keyword):
    keywords.append(keyword)


def remove_keyword(keyword):
    keywords.remove(keyword)


def clean_all_keywords():
    keywords = []
    print("\n已清空！\n")


def add(str, func):
    print("\n抵制不良信息，拒绝盗版内容!\n")
    print("\n每行输入" + str + "，输入‘0’时结束输入\n")
    while True:
        tmp_str = input(str + "：")
        if tmp_str is "0":
            return
        func(tmp_str)


def remove(str, container, func):
    if len(container) <= 0:
        print("\n已清空" + str + "！\n")
        return
    print("\n以下是您已经添加的" + str + "：\n")
    for item in container:
        print(item)
    print("\n每行输入要移除的" + str + ",输入‘0’时结束输入\n")
    while True:
        tmp_str = input(str + "：")
        if tmp_str is "0":
            return
        if tmp_str not in container:
            print("\n输入错误，请重新输入！\n")
            continue
        func(tmp_str)
        if len(container) <= 0:
            print("\n已清空" + str + "！\n")
            return


def tmp_menu(str):
    print("        编辑" + str)
    print(" - - - - - - - - - - - - - -")
    print("        1.增加" + str)
    print("        2.移除" + str)
    print("        3.清除全部")
    print("        0.返回主菜单")


def main_menu(str):
    tmp_str = "开启"
    if search_by_keywords is True:
        tmp_str = "关闭"
    print("        XX阅读")
    print(" - - - - - - - - - - - - - -")
    print("        1.搜索文章")
    print("        2.编辑源地址")
    print("        3.编辑关键词")
    print("        4." + tmp_str + "关键词搜索")
    print("        0.退出")
    print(" - - - - - - - - - - - - - -")
    print("        计XX-X XXX")
    print("        北方工业大学")


def format_menu(func, str):
    print("\n============================")
    func(str)
    print("============================")
    limit = 3
    if str is None:
        limit = 4
    while True:
        num = int(input("\n输入序号："))
        if num >= 0 and num <= limit:
            return num


def edit(str, container, func1, func2, func3):
    while True:
        num = format_menu(tmp_menu, str)
        if num is 1:
            add(str, func1)
        elif num is 2:
            remove(str, container, func2)
        elif num is 3:
            func3()
        else:
            print("\n返回主菜单!\n")
            break


def read_url_file(file_object):
    cnt = 0
    while True:
        url_name = file_object.readline().replace("\n", "")
        if not url_name:
            return
        url = file_object.readline().replace("\n", "")
        cnt += 1
        urls[url_name] = url


def write_url_file(file_object):
    for url_name in urls:
        file_object.write(url_name + "\n")
        file_object.write(urls[url_name] + "\n")


def read_keyword_file(file_object):
    cnt = 0
    while True:
        keyword = file_object.readline().replace("\n", "")
        if not keyword:
            break
        cnt += 1
        keywords.append(keyword)


def write_keyword_file(file_object):
    for keyword in keywords:
        file_object.write(keyword + "\n")


def file_operate(file_path, op, func):
    with open(file_path, op) as file_object:
        func(file_object)


def init():
    print("\nHELLO!\n")
    print("\n抵制不良信息，拒绝盗版内容。注意自我保护，谨防受骗上当。适度上网益脑，沉迷网络伤身。合理安排时间，享受健康生活。\n")
    if os.path.isfile(urls_path):
        file_operate(urls_path, 'r', read_url_file)
    if os.path.isfile(keywords_path):
        file_operate(keywords_path, 'r', read_keyword_file)


def end():
    print("\nBYE!\n")
    file_operate(urls_path, 'w', write_url_file)
    file_operate(keywords_path, 'w', write_keyword_file)


def build_soup(url):
    try:
        res = requests.get(url)
        try:
            res.raise_for_status()
        except Exception as exc:
            print("网络产生问题: {0}".format(exc))
        return bs4.BeautifulSoup(res.text, 'html.parser')
    except:
        pass


def include_keyword(str):
    flag = False
    for keyword in keywords:
        if keyword in str:
            flag = True
            break
    return flag


def get_article(url_name, url):
    cnt = 0
    paper = build_soup(url)
    if paper is not None:
        for item in paper.find_all("a", attrs={"href": True}):
            if item.string is not None and "http" in item.get("href") and (search_by_keywords is False or include_keyword(item.string)):
                article = build_soup(item.get("href"))
                if article is not None:
                    paragraphs = article.find_all("p")
                    if len(paragraphs) is not 0:
                        cnt += 1
                        print(url_name + "_" + item.string)
                        file_path = os.path.split(os.path.realpath(sys.argv[0]))[
                            0] + "\\" + re.sub(r"[\/\\\:\*\?\"\<\>\|]", "", url_name + "_" + item.string) + ".txt"
                        with open(file_path, "w", encoding="utf-8") as file_object:
                            for paragraph in paragraphs:
                                if paragraph.string is not None:
                                    file_object.write(
                                        paragraph.string + "\n\n")
    return cnt


def search_article():
    if len(urls) <= 0 or (search_by_keywords is True and len(keywords) <= 0):
        print("\n请先完善源地址或关键词！\n")
        return
    print("\n正在为您搜索文章......\n")
    cnt = 0
    for url_name in urls:
        url = urls[url_name]
        cnt += get_article(url_name, url)
    if cnt is 0:
        print("\n暂时没有文章，请稍后再试！\n")
    else:
        print("\n已结束搜索！合理安排时间，享受健康生活！\n")


init()

while True:
    num = format_menu(main_menu, None)
    if num is 1:
        search_article()
    elif num is 2:
        edit(url_str, urls, add_url, remove_url, clean_all_urls)
    elif num is 3:
        edit(keyword_str, keywords, add_keyword,
             remove_keyword, clean_all_keywords)
    elif num is 4:
        search_by_keywords = not search_by_keywords
    else:
        end()
        break
