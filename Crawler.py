import requests
import lxml
from bs4 import BeautifulSoup


def parse_site(sentence, count):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.naver.com/'}
    blog_lists = []
    for i in range(1, count + 1):
        try:
            site = requests.get('https://search.naver.com/search.naver?sm=tab_pge&where=post&ie=utf8' +
                                '&query=' + sentence +
                                '&start=' + str(i) +
                                '&post_blogurl=naver.com', headers=headers)

            soup = BeautifulSoup(site.text, 'lxml')
            parse_blog = soup.find_all("a", {"class": "sh_blog_title _sp_each_url _sp_each_title"})
            blog_lists.append(parse_blog[0]['href'].encode('utf-8'))
        except IndexError:
            continue
    return blog_lists


def parse_letter(blog_lists):
    string = []
    for blog_list in blog_lists:
        try:
            if not blog_list:
                continue
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'http://www.naver.com/'}
            site = requests.get(blog_list, headers=headers)
            soup = BeautifulSoup(site.text, 'lxml')
            frame = soup.find_all("frame", {"id": "mainFrame"})
            for Frame in frame:
                Frame_url = (Frame['src'].encode('utf-8'))
            site_url = ("http://blog.naver.com/" + Frame_url.decode('utf-8'))
            site_url = requests.get(site_url)
            soup1 = BeautifulSoup(site_url.text, 'lxml')
            soup2 = (soup1.find_all("p", {"class": "se_textarea"}))
            for a in soup2:
                string.append(a.text)

            soup2 = (soup1.find_all("div", {"id": "postViewArea"}))
            for a in soup2:
                string.append(a.text)
        except:
            continue

        for i in range(len(string)):
            string[i] = string[i].replace("\xa0", ' ').replace("\u200b", '').replace("\n", ' ')

    return string
