from itertools import product
from re import A
from bs4 import BeautifulSoup
import requests
import math
import json
from datetime import datetime

class Opinion:
    def __init__(self,product_id,opinion_text,author_name,recommended,score_count,credibility,purchase_date,review_date,upvotes,downvotes,advantages,disadvantages,product_name, data_entry_id):
        self.product_id = product_id
        self.opinion_text = opinion_text
        self.author_name = author_name
        self.recommended = recommended
        self.score_count = score_count
        self.credibility = credibility
        self.purchase_date = purchase_date
        self.review_date = review_date
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.advantages = advantages
        self.disadvantages = disadvantages
        self.product_name = product_name
        self.data_entry_id = data_entry_id
    
    def get_data(self):
        return {"product_id" : self.product_id,"author_name" : self.author_name, "opinion_text" : self.opinion_text,
        "recommended" : self.recommended, "score_count":self.score_count,
        "credibility" : self.credibility, "purchase_date" : self.purchase_date, "review_date" : self.review_date,
        "upvotes" : self.upvotes, "downvotes" : self.downvotes,
        "advantages" : self.advantages,"disadvantages" : self.disadvantages, "product_name" : self.product_name, "data_entry_id" : self.data_entry_id}

    def get_data_for_json(self):
        return {"product_id" : self.product_id,"author_name" : self.author_name, "opinion_text" : self.opinion_text,
        "recommended" : self.recommended, "score_count":self.score_count,
        "credibility" : self.credibility, "purchase_date" : str(self.purchase_date), "review_date" : str(self.review_date),
        "upvotes" : self.upvotes, "downvotes" : self.downvotes,
        "advantages" : self.advantages,"disadvantages" : self.disadvantages, "product_name" : self.product_name, "data_entry_id" : self.data_entry_id}

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
        product_name = soup.find("h1",{"class" : "product-top__product-info__name"}).get_text()
        opinion_page = 1

        for i in range(int(math.ceil(opinion_count/10))):
            url = f"https://www.ceneo.pl/{self.id}/opinie-{opinion_page}"
            req = requests.get(url, headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            
            temp_opinions = soup.find_all("div",{"class" : "user-post user-post__card js_product-review"})
            
            for opinion in temp_opinions:
                data_entry_id = opinion.attrs["data-entry-id"]
                author_name = opinion.find("span",{"class" : "user-post__author-name"}).get_text().capitalize()
                opinion_text = opinion.find("div",{"class" : "user-post__text"}).get_text().strip().capitalize()
                score_count = opinion.find("span",{"class" : "user-post__score-count"}).get_text()
                upvotes = opinion.find("button", {"class" : "vote-yes js_product-review-vote js_vote-yes"}).find("span").get_text()
                downvotes = opinion.find("button", {"class" : "vote-no js_product-review-vote js_vote-no"}).find("span").get_text()

                try:
                    credibility = opinion.find("div",{"class" : "review-pz"}).find("em").get_text()
                    credibility = True
                except:
                    credibility = False

                try:
                    recommended = opinion.find("span",{"class" : "user-post__author-recomendation"}).find("em").get_text()
                    if recommended == "Polecam":
                        recommended = True
                    else:
                        recommended = False
                except:
                    recommended = False


                dates = opinion.find("span",{"class" : "user-post__published"}).find_all("time")
                purchase_date = dates[0].attrs["datetime"]
                purchase_date = datetime.strptime(purchase_date,"%Y-%m-%d %H:%M:%S")
                if len(dates) > 1:
                    review_date = dates[1].attrs["datetime"]
                    review_date = datetime.strptime(review_date,"%Y-%m-%d %H:%M:%S")
                
                columns = opinion.find_all("div",{"class" : "review-feature__col"})
                advantages = ""
                disadvantages = ""
                if len(columns) > 0:
                    advantages = []
                    col1 = columns[0].find_all("div",{"class" : "review-feature__item"})
                    for comment in col1:
                        advantages.append(comment.get_text())
                    advantages = ','.join(advantages)
                if len(columns) == 2:
                    disadvantages = []
                    col2 = columns[1].find_all("div",{"class" : "review-feature__item"})
                    for comment in col2:
                        disadvantages.append(comment.get_text())
                    disadvantages = ','.join(disadvantages)

                self.add_opinion(Opinion(self.id,opinion_text,author_name,recommended,score_count,credibility,purchase_date,review_date,upvotes,downvotes,advantages,disadvantages,product_name, data_entry_id))
                print(str(opinion_text), end="\n\n")

            opinion_page += 1
        return self.opinions

    def get_opinions(self):
        return self.opinions
    
    def get_id(self):
        return self.id

    def create_json(self):
        json_obj = {"all_opinions" : []}
        data_array = []
        for opinion in self.opinions:
            data = opinion.get_data_for_json()
            data_array.append(data)

        json_obj["all_opinions"].append({"id" : self.id, "opinions" : data_array})
        return json.dumps(json_obj, indent = 4, ensure_ascii=False).encode('utf8')

#prod = Product("87640813")
#data = prod.download_opinions()
#prod.create_json()

print("hello")