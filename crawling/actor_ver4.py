import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
from collections import ChainMap

# 영화제목
movie_list = []
# 배우이름
actor_list = []
# 수상여부
award_list = []
# 배우 url (m)
actor_url_list = []

imdb_list = []

# goldenglobe
golden_list = []
critic_list = []
sag_list = []

winner_list = []
nomi1_list = []
nomi2_list = []
nomi3_list = []
nomi4_list = []

v_list = [0, 0, 0, 0, 0, 1, 2, 0, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 0, 2, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0,
          2, 1, 0, 1, 1,
          1, 0, 2, 1, 1, 2, 1, 0, 1, 2, 1, 1, 1, 0, 2, 0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 1, 2, 1, 1, 1, 1, 2, 1, 1,
          1, 1, 2, 0, 1,
          1, 1, 2, 1, 1, 0, 1, 2, 1, 1, 0, 1, 2, 0, 1, 0, 1, 2, 1, 0, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 1, 2, 2, 1, 0, 1, 1,
          2, 1, 1, 0, 1]
for i in range(321):
    sag_list.append("-")

for j in range(len(v_list)):
    sag_list.append(v_list[j])

value_list = [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 1, 0,
              0, 0, 0, 2, 0,
              2, 1, 1, 0, 1, 2, 1, 1, 1, 0, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1,
              2, 0, 1, 1, 1,
              1, 0, 2, 0, 1, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 0, 0, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 2, 1, 1, 1, 0,
              1, 2, 1, 1, 1]
for i in range(327):
    critic_list.append("-")

for j in range(len(value_list)):
    critic_list.append(value_list[j])

# no goldenglobe
for i in range(67):
    golden_list.append("-")

# 1944
for i in range(67, 68):
    golden_list.append(2)

for i in range(68, 72):
    golden_list.append(0)

# no goldenglobe
for i in range(15):
    winner_list.append("-")
    nomi1_list.append("-")
    nomi2_list.append("-")
    nomi3_list.append("-")
    nomi4_list.append("-")

# 1944
for i in range(15, 16):
    winner_list.append(0)
    nomi1_list.append(0)
    nomi2_list.append(0)
    nomi3_list.append(0)
    nomi4_list.append(0)

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

# movie list
for m in movies:
    movie = m.select_one("i").text
    try:
        for i in range(int(m.attrs["rowspan"])):
            movie_list.append(movie)
    except:
        movie_list.append(movie)

    if movie == "The Defiant Ones" or movie == "The Wrestler":
        imdb_list.append("-")

    else:
        movie = m.select_one("i")
        # genre link
        try:
            url = movie.select_one("a").attrs["href"]
            raw_movie = requests.get("https://en.wikipedia.org" + url, headers={"User-Agent": "Mozilla/5.0"})
            html_movie = BeautifulSoup(raw_movie.text, 'html.parser')

            imdbs = html_movie.select("div.mw-parser-output ul li")

            for i in imdbs:
                if "IMDb" in i.text:
                    imdb = i.select_one("a:nth-of-type(1)")
                    imdb_list.append(imdb.attrs["href"])

                    if m.attrs["rowspan"] == "2":
                        imdb_list.append(imdb.attrs["href"])

                    else:
                        continue
                else:
                    continue

        except:
            continue

# actor list # name # awarded
for actor in actors:
    name = actor.select_one("span a")
    actor_list.append(name.text)
    # actor url 0~466
    actor_url_list.append(name.attrs["href"])
    try:
        actor.attrs["style"] == "background:#FAEB86;"
        award_list.append(1)
    except:
        award_list.append(0)

def get_genre(index):
    if imdb_list[index] != "-":
        raw_imdb = requests.get(imdb_list[index], headers={"User-Agent": "Mozilla/5.0"})
        html_imdb = BeautifulSoup(raw_imdb.text, 'html.parser')

        genres = html_imdb.select("div#titleStoryLine div:nth-of-type(4) a")

        genre = ""
        for g in genres:
            genre += g.text + " "
        # genre_list.append(genre)
        return {index: genre}
    else:
        # genre_list.append("-")
        return {index: "-"}

def get_boxoffice_budget(index):
    global movie_list
    try:
        raw_box = get_raw("https://www.boxofficemojo.com/search/?q=" + movie_list[index])
        print(movie_list[index])
        html_box = BeautifulSoup(raw_box.text, 'html.parser')
        result = html_box.select_one("a.a-size-medium.a-link-normal.a-text-bold")
        print("result값은", result.text)
        if result.text == movie_list[index]:
            print("들어옴")
            url = result.attrs["href"]

            raw_result = get_raw("https://www.boxofficemojo.com" + url)
            html_result = BeautifulSoup(raw_result.text, 'html.parser')

            try:
                revenue_box = html_result.select_one(
                    "div.a-section.a-spacing-none.mojo-performance-summary-table div:nth-of-type(3) span.a-text-bold span.money").text
                print(result.text+"boxoffice")
            except:
                revenue_box = "-"

            try:
                revenue_budget = html_result.select_one(
                    "div.a-section.a-spacing-none.mojo-summary-values.mojo-hidden-from-mobile div:nth-of-type(3) span.money").text
            except:
                revenue_budget = "-"

            revenue_box = revenue_box[1:].replace(",", "")
            revenue_budget = revenue_budget[1:].replace(",", "")
        else:
            revenue_box = "-"
            revenue_budget = "-"
    except:
        revenue_box = "-"
        revenue_budget = "-"
        return {index: (revenue_box, revenue_budget)}
    return {index: (revenue_box, revenue_budget)}


def get_name_age(index):
    global actor_url_list
    raw_each = get_raw("https://en.wikipedia.org" + actor_url_list[index])
    html_each = BeautifulSoup(raw_each.text, 'html.parser')
    try:
        age = html_each.select_one("table.vcard span.bday").text
        return {index: age[:4]}
        # age_list.append(age[:4])
    except:
        # age_list.append("-")
        return {index: "-"}

def get_rate(index):
    global movie_list

    for i in range(len(movie_list)):
        movie_list[i] = movie_list[i].replace(" ", "_")

    raw_mov = get_raw("https://www.rottentomatoes.com/m/" + movie_list[index])
    html_mov = BeautifulSoup(raw_mov.text, 'html.parser')
    try:
        rate = html_mov.select_one("div.mop-ratings-wrap__half h2 a span:nth-of-type(2)").text[21:23]
        # rate_list.append(rate)
        return {index:rate}
    except:
        # rate_list.append("-")
        return {index:"-"}

if __name__ == '__main__':
    f = open("final_actor.csv", "w", encoding="utf-8", newline='')
    wr = csv.writer(f)
    wr.writerow(["movie", "name", "age", "awarded", "genre", "rate", "boxoffice", "budget", "goldenglobe", "critic", "sag"])

    p = Pool(30)

    r = p.map_async(get_boxoffice_budget, range(len(movie_list)))
    result = r.get()
    boxoffice_budget = dict(ChainMap(*result))
    # dic 잘 나왔는지
    print(boxoffice_budget)
    print(len(boxoffice_budget))

    r = p.map_async(get_name_age, range(len(actor_list)))
    result = r.get()
    age = dict(ChainMap(*result))
    # dic 잘 나왔는지
    print(age)
    print(len(age))

    r = p.map_async(get_genre, range(len(imdb_list)))
    result = r.get()
    genre = dict(ChainMap(*result))
    # dic 잘 나왔는지
    print(genre)
    print(len(genre))

    r = p.map_async(get_rate, range(len(movie_list)))
    result = r.get()
    rate = dict(ChainMap(*result))
    # dic 잘 나왔는지
    print(rate)
    print(len(rate))

    for p in range(18, -1, -1):
        raw_golden = get_raw("https://www.goldenglobes.com/winners-nominees/best-performance-actor-motion-picture-drama?page=" + str(p))
        html_golden = BeautifulSoup(raw_golden.text, 'html.parser')

        # winner list
        winner = html_golden.select("div.view-grouping-content div.views-row-1 div.primary-nominee")
        winner.reverse()

        for w in winner:
            win = w.select_one("a").text
            winner_list.append(win)

        # nomini list 1
        nomi1 = html_golden.select("div.view-grouping-content div.views-row-2 div.primary-nominee")
        nomi1.reverse()
        if nomi1 == []:
            nomi1_list.append("-")
            nomi1_list.append("-")
            nomi1_list.append("-")
            nomi1_list.append("-")

        elif len(nomi1) != 4:
            if len(nomi1) == 1:
                nomi1_list.append("-")
                nomi1_list.append("-")
                nomi1_list.append("-")
            elif len(nomi1) == 2:
                nomi1_list.append("-")
                nomi1_list.append("-")
            else:
                nomi1_list.append("-")
            for n1 in nomi1:
                nomini1 = n1.select_one("a").text
                nomi1_list.append(nomini1)
        else:
            for n1 in nomi1:
                nomini1 = n1.select_one("a").text
                nomi1_list.append(nomini1)

        # nomini list 2
        nomi2 = html_golden.select("div.view-grouping-content div.views-row-3 div.primary-nominee")
        nomi2.reverse()
        if nomi2 == []:
            nomi2_list.append("-")
            nomi2_list.append("-")
            nomi2_list.append("-")
            nomi2_list.append("-")

        elif len(nomi2) != 4:
            if len(nomi2) == 1:
                nomi2_list.append("-")
                nomi2_list.append("-")
                nomi2_list.append("-")
            elif len(nomi2) == 2:
                nomi2_list.append("-")
                nomi2_list.append("-")
            else:
                nomi2_list.append("-")
            for n2 in nomi2:
                nomini2 = n2.select_one("a").text
                nomi2_list.append(nomini2)
        else:
            for n2 in nomi2:
                nomini2 = n2.select_one("a").text
                nomi2_list.append(nomini2)

        # nomini list 3
        nomi3 = html_golden.select("div.view-grouping-content div.views-row-4 div.primary-nominee")
        nomi3.reverse()
        if nomi3 == []:
            nomi3_list.append("-")
            nomi3_list.append("-")
            nomi3_list.append("-")
            nomi3_list.append("-")

        elif len(nomi3) != 4:
            if len(nomi3) == 1:
                nomi3_list.append("-")
                nomi3_list.append("-")
                nomi3_list.append("-")
                nomi3_list.append("-")
            elif len(nomi3) == 2:
                nomi3_list.append("-")
                nomi3_list.append("-")
            else:
                nomi3_list.append("-")
            for n3 in nomi3:
                nomini3 = n3.select_one("a").text
                nomi3_list.append(nomini3)
        else:
            for n3 in nomi3:
                nomini3 = n3.select_one("a").text
                nomi3_list.append(nomini3)

        # nomini list 4
        nomi4 = html_golden.select("div.view-grouping-content div.views-row-5 div.primary-nominee")
        nomi4.reverse()
        if nomi4 == []:
            nomi4_list.append("-")
            nomi4_list.append("-")
            nomi4_list.append("-")
            nomi4_list.append("-")

        elif len(nomi4) != 4:
            if len(nomi4) == 1:
                nomi4_list.append("-")
                nomi4_list.append("-")
                nomi4_list.append("-")
            elif len(nomi4) == 2:
                nomi4_list.append("-")
                nomi4_list.append("-")
            else:
                nomi4_list.append("-")
            for n4 in nomi4:
                nomini4 = n4.select_one("a").text
                nomi4_list.append(nomini4)
        else:
            for n4 in nomi4:
                nomini4 = n4.select_one("a").text
                nomi4_list.append(nomini4)

    cnt = 1
    for i in range(72, 447, 5):
        for j in range(5):
            if actor_list[i + j] == winner_list[i - (52 + 4 * cnt)]:
                golden_list.append(2)
            elif actor_list[i + j] == nomi1_list[i - (52 + 4 * cnt)]:
                golden_list.append(1)
            elif actor_list[i + j] == nomi2_list[i - (52 + 4 * cnt)]:
                golden_list.append(1)
            elif actor_list[i + j] == nomi3_list[i - (52 + 4 * cnt)]:
                golden_list.append(1)
            elif actor_list[i + j] == nomi4_list[i - (52 + 4 * cnt)]:
                golden_list.append(1)
            else:
                golden_list.append(0)
        cnt += 1

    for i in range(0, 447):
        boxoffice = boxoffice_budget[i][0]
        budget = boxoffice_budget[i][1]
        wr.writerow([movie_list[i], actor_list[i], age[i], award_list[i], genre[i], rate[i], boxoffice, budget, golden_list[i], critic_list[i], sag_list[i]])

    f.close()