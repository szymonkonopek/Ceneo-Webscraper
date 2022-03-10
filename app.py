from asyncio import tasks
from urllib import request
from flask import Flask, render_template, url_for, request, redirect ,Response
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from soup import Product
import pandas as pd
from unidecode import unidecode
from IPython.core.display import display, HTML

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ceneo.db'
db = SQLAlchemy(app)

class Ceneo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data_entry_id = db.Column(db.String(200), nullable = False)
    product_id = db.Column(db.String(200), nullable = False)
    author_name = db.Column(db.String(200), nullable = False)
    opinion_text = db.Column(db.String(200), nullable = False)
    recommended = db.Column(db.Boolean, nullable = False)
    score_count = db.Column(db.String(200), nullable = False)
    credibility = db.Column(db.Boolean(200), nullable = False)
    upvotes = db.Column(db.String(200), nullable = False)
    downvotes = db.Column(db.String(200), nullable = False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
    review_date = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
    advantages = db.Column(db.String(200), nullable = False)
    disadvantages = db.Column(db.String(200), nullable = False)
    product_name = db.Column(db.String(200), nullable = False)
    

    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class SortableTable(Table):
    author = Col('AUTHOR')
    opinion = Col('OPINION')
    rating = Col('RATING')
    usefulnes = Col("USEFULNESS")
    upsides = Col('UPSIDES')
    downsides = Col("DOWNSIDES")
    confirmed = Col('CONFIRMED')
    date = Col("REVIEW")
    usage = Col("PURCHASE")
    review = Col("TEXT")

    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for(request.endpoint, **request.view_args, sort=col_key, direction=direction, _anchor='main-table')

@app.route('/extraction',methods = ['POST', 'GET'])
def extraction():
    if request.method == "POST":
        old_tasks = Ceneo.query.order_by(Ceneo.date_created).all()
        form_content = request.form['content'] #content z form z html
        try:
            prod_obj = Product(form_content)
            opinions = prod_obj.download_opinions()
            tasks = []
            
            comments_ids = []
            for old_task in old_tasks:
                if old_task.product_id == opinions[0].get_data()["product_id"]:
                    comments_ids.append(old_task.data_entry_id)
            

            for opinion in opinions:
                data = opinion.get_data()
                if (data["data_entry_id"] in comments_ids):
                    continue

                author_name = data["author_name"]
                opinion_text = data["opinion_text"]
                product_id = data["product_id"]
                recommended = data["recommended"]
                score_count = data["score_count"]
                credibility = data["credibility"]
                upvotes = data["upvotes"]
                downvotes = data["downvotes"]
                purchase_date = data["purchase_date"]
                review_date = data["review_date"]
                advantages = data["advantages"]
                disadvantages = data["disadvantages"]
                product_name = data["product_name"]
                data_entry_id = data["data_entry_id"]

                task = Ceneo(author_name = author_name, opinion_text = opinion_text, product_id = product_id,
                recommended = recommended, score_count=score_count, credibility=credibility,upvotes=upvotes,
                downvotes=downvotes,purchase_date=purchase_date,review_date=review_date,advantages=advantages,
                disadvantages=disadvantages, product_name = product_name, data_entry_id = data_entry_id)
                tasks.append(task)
        
            for task in tasks:
                db.session.add(task)
            db.session.commit()
            return redirect(f'/product-page/{prod_obj.id}')
        except Exception as e:
            print(e)
            return render_template('extraction.html', error = "Something went wrong :(")

    else:
        tasks = Ceneo.query.order_by(Ceneo.date_created).all()
        return render_template('extraction.html', tasks = tasks)


@app.route('/delete/<int:product_id>/<int:id>/<int:length>')
def delete(product_id,id,length):
    task_to_delete = Ceneo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        if length > 1:
            return redirect(f'/product-page/{product_id}')
        else:
            return redirect('/product-list')
    except:
        return "There was an error :("

@app.route('/delete-page/<int:id>')
def delete_page(id):
    tasks = Ceneo.query.order_by(Ceneo.date_created).all()
    tasks_ids = []
    for task in tasks:
        if task.product_id == str(id):
            tasks_ids.append(task.id)
    for id in tasks_ids:
        try:
            task_to_delete = Ceneo.query.get_or_404(id)
            db.session.delete(task_to_delete)
            db.session.commit()
        except:
            print("problem")
    return redirect("/product-list")

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Ceneo.query.get_or_404(id)

    if request.method == 'POST':
        task.author_name = request.form['content']

        try:
            db.session.commit()
            return redirect('/extraction')
        except:
            return "Error updating :("
    else:
        return render_template('update.html',task = task)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product-list')
def product_list():
    tasks = Ceneo.query.order_by(Ceneo.date_created).all()
    unique_ids = []
    unique_products = []

    def to_float(score):
        score = score[:-2]
        score = score.replace(",",".")
        return float(score)


    for task in tasks:
        if task.product_id not in unique_ids:
            unique_ids.append(str(task.product_id))
            opinions = Ceneo.query.order_by(Ceneo.date_created).filter(Ceneo.product_id == task.product_id)
            number_of_downsides = 0
            number_of_upsides = 0
            score_sum = 0
            for opinion in opinions:
                number_of_upsides += len(opinion.advantages.split(',')) if len(opinion.advantages) > 1 else 0
                number_of_downsides += len(opinion.disadvantages.split(',')) if len(opinion.disadvantages) > 1 else 0
                score_sum += to_float(opinion.score_count)

            unique_products.append({"id": task.product_id,"name": task.product_name, "number_of_opinions" : opinions.count(), "number_of_downsides" : number_of_downsides, "number_of_upsides" : number_of_upsides, "average_score" : round(score_sum/opinions.count(),1) })

    return render_template('product-list.html', unique_products = unique_products)

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/product-page/<int:id>', methods = ['GET','POST'])
def product_page(id):
    
    
    filter_text = False
    filter_category = False
    product_name = ""
    anchor = ""
    
    if request.method == "POST":
        filter_text = request.form['filter_text'] #content z form z html
        filter_category = request.form['filter_category'] #content z form z html

    
    if filter_text and filter_category:
        tasks = Ceneo.query.order_by(Ceneo.date_created).filter(eval(str(getattr(Ceneo,filter_category))).contains(filter_text))
        anchor = "main-table"
    else:
        tasks = Ceneo.query.order_by(Ceneo.date_created).all() 
    

    tasks_array = []
    for task in tasks:
        if task.product_id == str(id):
            task_array = []
            task_array.append(unidecode(task.author_name))
            task_array.append("POSITIVE" if task.recommended else "NEGATIVE")
            task_array.append(task.score_count)
            task_array.append(int(task.upvotes)-int(task.downvotes))
            task_array.append(f"({len(task.advantages.split(',')) if len(task.advantages) > 1 else 0}) {task.advantages}")
            task_array.append(f"({len(task.disadvantages.split(',')) if len(task.disadvantages) > 1 else 0}) {task.disadvantages}")
            task_array.append("Yes" if task.credibility else "No")
            task_array.append(str(task.review_date))
            task_array.append(str(task.purchase_date))
            task_array.append(unidecode(task.opinion_text))
            product_name = task.product_name

            tasks_array.append(task_array)
    
    df = pd.DataFrame(tasks_array, columns=["author", "opinion", "rating", "usefulnes", "upsides", "downsides", "confirmed", "date", "usage", "review"])

    sort = request.args.get('sort', 'author')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    df = df.sort_values(by=[sort], ascending=reverse)
    output_dict = df.to_dict(orient='records')

    sort_table = SortableTable(output_dict,sort_by=sort,sort_reverse=reverse)
    
    return render_template('product-page.html', id = str(id), sort_table = sort_table, product_name = product_name, anchor = anchor)
        
@app.route('/product-page/<int:id>/charts')
def charts(id):
    tasks = Ceneo.query.order_by(Ceneo.date_created).all()
    tasks_array = []
    positive = 0
    num_of_cur_prod = 0
    num_of_char = 0
    score = 0
    confirmed_purchases = 0

    def to_float(score):
        score = score[:-2]
        score = score.replace(",",".")
        return float(score)

    for task in tasks:
        if task.product_id == str(id):
            num_of_cur_prod += 1
            tasks_array.append(task)
            num_of_char += len(task.opinion_text)
            score += to_float(task.score_count)
            if task.recommended == True:
                positive += 1
            if task.credibility == True:
                confirmed_purchases += 1

    def get_labels_and_values(col):
        unique_items = []
        item_count = []

        for item1 in col:
            if str(item1) not in unique_items:
                unique_items.append(str(item1))

                count = 0
                for item2 in col:
                    if (str(item1) == str(item2)):
                        count += 1
                item_count.append(count)

        next = True
        while next:
            skip = True
            for i in range(len(item_count)-1):
                if item_count[i] < item_count[i+1]:
                    temp = item_count[i]
                    item_count[i] = item_count[i+1]
                    item_count[i+1] = temp

                    temp = unique_items[i]
                    unique_items[i] = unique_items[i+1]
                    unique_items[i+1] = temp
                    skip = False
            if skip:
                next = False
            
        
        return {"items": unique_items,"count":item_count}

    def get_updowns(updowns):
        all_updown_elements = []
        for updown in updowns:
            updown_list = updown.split(",")
            for updown_list_el in updown_list:
                if len(updown_list_el) > 1:
                    all_updown_elements.append(updown_list_el)
        return all_updown_elements

    satisfaction = str(int((positive/num_of_cur_prod)*100)) +  "%"
    
    recommend = get_labels_and_values([row.recommended for row in tasks_array])
    rating = get_labels_and_values([to_float(row.score_count) for row in tasks_array])
    confirmed = get_labels_and_values([row.credibility for row in tasks_array])
    upsides = get_labels_and_values(get_updowns([row.advantages for row in tasks_array]))
    downsides = get_labels_and_values(get_updowns([row.disadvantages for row in tasks_array]))
    data = {"recommend" : recommend, "rating" : rating, "confirmed" : confirmed, "upsides" : upsides, "downsides" : downsides }
    stats = {"satisfaction" : satisfaction, "num_of_char" : num_of_char,"average_char" : int(num_of_char/num_of_cur_prod) , "average_score" : round(float(score/num_of_cur_prod),1), "num_of_cur_prod" : num_of_cur_prod, "confirmed" : round((confirmed_purchases/num_of_cur_prod)*100,1)}

    return render_template('charts.html', id = str(id), tasks = tasks_array,data = data, stats = stats)

@app.route('/download-json/<int:id>/')
def download_json(id):
    prod = Product(id)
    data = prod.download_opinions()
    content = prod.create_json()
    return Response(content, 
            mimetype='application/json',
            headers={'Content-Disposition':f'attachment;filename={id}.json'})

if __name__ == "__main__":
    app.run(debug = True)

