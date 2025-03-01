import re
import time
import random
import pymysql
import urllib.request
import urllib.error
import numpy as np

send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        }

def get_url():
    with open("movie_set.txt", "r", encoding="utf-8") as fp:
        urls = []
        for line in fp:
            for start in range(0, 181, 20):
                url = line.strip().split(" ")[0]
                url = url + "comments?start=" + str(start) + "&limit=20&sort=new_score&status=P"
                urls.append(url)
        return urls

def get_element(url, db):
    cur = db.cursor()
    user_flag = re.compile(r'a title="(.+?)"')
    date_flag = re.compile(r'\d{4}-\d+-\d+')
    score_flag = re.compile(r'allstar(.+?) ')
    comment_flag = re.compile('<span class="short">(.+?)</span>')

    req = urllib.request.Request(url, headers=send_headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            htmls = response.read()
    except urllib.error.URLError as e:
        # print(f"URL error: {e}")
        return

    title_flag = re.compile(r'<h1.*?>(.*?)</h1>')
    title = title_flag.findall(htmls.decode('utf-8'))[0].split(" ")[0]

    module = []
    while True:
        begin = htmls.find(b'<div class="avatar">')
        end = begin + 10 + htmls[begin + 10:].find(b'<div class="avatar">')
        if end == 8:
            break
        module.append(htmls[begin:end])
        htmls = htmls[end:]
    module = module[:-1]
    
    for ele in module:
        ele = " ".join(ele.decode('utf-8').split("\n"))
        username = user_flag.findall(ele)

        if len(username) != 0:
            username = username[0].strip()
            # print(username)
        else:
            continue
        dates = date_flag.findall(ele)
        if len(dates) != 0:
            dates = dates[0].strip()
            # print(dates)
        else:
            continue
        score = score_flag.findall(ele)
        if len(score) != 0:
            score = str(int(score[0].strip())/10)
            # print(score)
        else:
            continue
        comment = comment_flag.findall(ele)
        if len(comment) != 0:
            comment = comment[0].strip()
            # print( comment)
        else:
            continue

        sql = "INSERT INTO comments_new \
                (username, title, date, score, comment) \
                VALUES (%s, %s, %s, %s, %s);"
        try:
            cur.execute(sql, (username, title, dates, score, comment))
            db.commit()
            print("写入成功")
        except Exception as e:
            print(f"数据库写入出错: {e}")
            db.rollback()
    cur.close()

# 去除重复影评
def get_newdb(db):
    cur_r = db.cursor()
    cur_w = db.cursor()
    sql = "SELECT distinct * FROM comments_new order by title;"
    cur_r.execute(sql)
    x = 0
    for ele in cur_r:
        x += 1
        print(f"{x}")
        line = list(ele)
        username = line[0]
        title = line[1]
        dates = line[2]
        score = int(line[3])
        comment = line[4]
        sql = "INSERT INTO movies_new \
                (username, title, date, score, comment) \
                VALUES (%s, %s, %s, %s, %s);"
        try:
            cur_w.execute(sql, (username, title, dates, score, comment))
            db.commit()
        except Exception as e:
            print(f"数据库写入出错: {e}")
            db.rollback()
    cur_r.close()
    cur_w.close()

if __name__ == "__main__":
    db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="douban", charset='utf8')

    # 爬取影评和评分
    urls = get_url()
    urls = urls[:1000]
    x = 0
    for url in urls:
        x += 1
        print(f"{url} {x}/{len(urls)}")
        try:
            get_element(url, db)
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            continue

    db.close()
