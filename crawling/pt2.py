import requests
from bs4 import BeautifulSoup

# 영화제목
movie_list = []
# 배우이름
actor_list = []
# 수상여부
award_list = []
# 배우 url (m)
actor_url_list = []
# 영화연도
year_list = []

imdb_list = []

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

raw = get_raw("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor")
html = BeautifulSoup(raw.text, 'html.parser')

movies = html.select("table:nth-of-type(3) tr td:nth-of-type(3)")
actors = html.select("table:nth-of-type(3) tr td:nth-of-type(1)")
years = html.select("table:nth-of-type(3) tbody > tr th")[5:]
print(years)

# year list
for y in years:
    year = y.text
    print(year)
    for i in range(int(y.attrs["rowspan"])):
        year_list.append(year.replace("ote 1]", "")[:-8])

for i in range(24):
    print(i)
    print(year_list[i])

    tmp = int(year_list[i].split("/")[0])+1
    del year_list[i]
    year_list.insert(i, tmp)

print(year_list)
# for i in range(14):
#     year_list[i].slice[]


# for i in range(1928, 2019):
#     year_list.append(i)
#
# print(year_list)

# movie list
for m in movies:
    movie = m.select_one("i").text
    try:
        for i in range(int(m.attrs["rowspan"])):
            movie_list.append(movie)
    except:
        movie_list.append(movie)

print(movie_list)