import re
from bs4 import BeautifulSoup
import requests

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


url = "https://www.ceneo.pl/104942408/opinie-1"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

num_of_opinions = soup.find("a",{"class" : "product-review__link link link--accent js_reviews-link js_clickHash js_seoUrl"})
opinion_count = int(num_of_opinions.find("span"))

opinions = soup.find_all("div",{"class" : "user-post user-post__card js_product-review"})

for opinion in opinions:
    review = opinion.find("div",{"class" : "user-post__text"}).string

    if review != None:
        print(str(review))