from itertools import product
from bs4 import BeautifulSoup
import requests
import math
import json

class Opinion:
    def __init__(self,opinion_text,author_name):
        self.opinion_text = opinion_text
        self.author_name = author_name
    
    def get_data(self):
        return {"author_name" : self.author_name, "opinion_text" : self.opinion_text}

class Product:
    def __init__(self,id):
        self.id = id
        self.opinions = []
    
    def add_opinion(self,opinion):
        self.opinions.append(opinion)

    def download_opinions(self):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }

        url = f"https://www.ceneo.pl/{self.id}/opinie-1"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        count_element = soup.find("a",{"class" : "product-review__link link link--accent js_reviews-link js_clickHash js_seoUrl"})
        opinion_count = int(count_element.find("span").string)

        opinion_page = 1

        for i in range(int(math.ceil(opinion_count/10))):
            url = f"https://www.ceneo.pl/{self.id}/opinie-{opinion_page}"
            req = requests.get(url, headers)
            soup = BeautifulSoup(req.content, 'html.parser')

            temp_opinions = soup.find_all("div",{"class" : "user-post user-post__card js_product-review"})
            
            for opinion in temp_opinions:
                author_name = opinion.find("span",{"class" : "user-post__author-name"}).get_text()
                opinion_text = opinion.find("div",{"class" : "user-post__text"}).get_text()
                self.add_opinion(Opinion(opinion_text,author_name))

                print(str(opinion_text), end="\n\n")

            opinion_page += 1
        return self.opinions

    def get_opinions(self):
        return self.opinions

    def create_json(self):
        json_obj = {"all_opinions" : []}
        data_array = []
        for opinion in self.opinions:
            data = opinion.get_data()
            data_array.append(data)

        json_obj["all_opinions"].append({"id" : self.id, "opinions" : data_array})
        return json.dumps(json_obj, indent = 4)
