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
