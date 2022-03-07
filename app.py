from asyncio import tasks
from urllib import request
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from soup import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ceneo.db'
db = SQLAlchemy(app)

class Ceneo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.String(200), nullable = False)
    author_name = db.Column(db.String(200), nullable = False)
    opinion_text = db.Column(db.String(200), nullable = False)
    recommended = db.Column(db.Boolean, nullable = False)
    score_count = db.Column(db.String(200), nullable = False)
    credibility = db.Column(db.String(200), nullable = False)
    upvotes = db.Column(db.String(200), nullable = False)
    downvotes = db.Column(db.String(200), nullable = False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
    review_date = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
    advantages = db.Column(db.String(200), nullable = False)
    disadvantages = db.Column(db.String(200), nullable = False)

    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/extraction',methods = ['POST', 'GET'])
def extraction():
    if request.method == "POST":
        form_content = request.form['content'] #content z form z html
        try:
            print("done")
            prod_obj = Product(form_content)
            opinions = prod_obj.download_opinions()
            tasks = []
            

            for opinion in opinions:
                data = opinion.get_data()
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

                task = Ceneo(author_name = author_name, opinion_text = opinion_text, product_id = product_id, recommended = recommended, score_count=score_count, credibility=credibility,upvotes=upvotes,downvotes=downvotes,purchase_date=purchase_date,review_date=review_date,advantages=advantages,disadvantages=disadvantages)
                tasks.append(task)

        
            for task in tasks:
                db.session.add(task)
            db.session.commit()
            return redirect(f'/product-page/{prod_obj.id}')
        except Exception as e:
            return str(e)

    else:
        tasks = Ceneo.query.order_by(Ceneo.date_created).all() #zwraca wszystkie elementy posortowane po dacie stworzenia (all wszystkie , first pierwsze)
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
    tasks = Ceneo.query.order_by(Ceneo.date_created).all() #zwraca wszystkie elementy posortowane po dacie stworzenia (all wszystkie , first pierwsze)
    unique_products = []
    for task in tasks:
        if task.product_id not in unique_products:
            unique_products.append(str(task.product_id))
        
    return render_template('product-list.html', unique_products = unique_products)

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/product-page/<int:id>', methods = ['GET','POST'])
def product_page(id):
    tasks = Ceneo.query.order_by(Ceneo.date_created).all() #zwraca wszystkie elementy posortowane po dacie stworzenia (all wszystkie , first pierwsze)
    return render_template('product-page.html',tasks = tasks, id = str(id))

if __name__ == "__main__":
    app.run(debug = True)

