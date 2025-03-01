import re
import time
import urllib.request
import urllib.error
TIMEOUT = 30

# 获取电影标签
def get_movie_label():
    tags = []
    tag_flag = re.compile(r'href="(.+?)"')
    with urllib.request.urlopen("https://movie.douban.com/tag/?view=cloud", timeout=TIMEOUT) as response:
        htmls = response.read().decode('utf-8')
    
    for line in htmls.split("\n"):
        if line.strip().find('href="/tag/') != -1:
            tag = "https://movie.douban.com" + tag_flag.findall(line.strip())[0]
            print(tag)
            tags.append(tag)
            for i in range(20, 141, 20):
                tags.append(tag + "?start=" + str(i) + "&type=T")
    return tags

# 获取电影链接和名称
def get_movie(tag):
    movies = []
    movie_flag = re.compile(r'nbg" href="(.+?)" ')
    name_flag = re.compile(r'title="(.+?)"')
    with urllib.request.urlopen(tag, timeout=TIMEOUT) as response:
        htmls = response.read().decode('utf-8')
    
    for line in htmls.split("\n"):
        if line.strip().find("nbg") != -1:
            movie_url = movie_flag.findall(line.strip())[0]
            movie_name = name_flag.findall(line.strip())[0]
            print(movie_url, movie_name)
            movies.append([movie_url, movie_name])
    return movies

# 去掉重复的电影，写入新的文件
def list2set():
    with open("movie_list.txt", "r", encoding="utf-8") as fp, open("movie_set.txt", "w", encoding="utf-8") as fout:
        movie_dict = {}
        for line in fp:
            movie_id = line.strip().split(" ")[0].split("/")[-2]
            if movie_id not in movie_dict:
                movie_dict[movie_id] = 1
                fout.write(line)

if __name__ == "__main__":
    tags = get_movie_label()
    with open("movie_list.txt", "w", encoding="utf-8") as fp:
        x = 0
        for tag in tags:
            x += 1
            print(tag + " " + str(x) + "/" + str(len(tags)))
            try:
                movies = get_movie(tag)
                for movie in movies:
                    fp.write(" ".join(movie) + "\n")
                time.sleep(2)
            except Exception as e:
                print(f"Error: {e}")
                continue

    # 去掉重复的电影
    time.sleep(5)    
    list2set()
