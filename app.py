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
    author_name = db.Column(db.String(200), nullable = False)
    opinion_text = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        form_content = request.form['content'] #content z form z html
        try:
            if form_content == None or "":
                return
            opinions = Product(form_content).download_opinions()
            tasks = []
            
            for opinion in opinions:
                data = opinion.get_data()
                author_name = data["author_name"]
                opinion_text = data["opinion_text"]
                task = Ceneo(author_name = author_name, opinion_text = opinion_text)
                tasks.append(task)

        
            for task in tasks:
                db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue :("

    else:
        tasks = Ceneo.query.order_by(Ceneo.date_created).all() #zwraca wszystkie elementy posortowane po dacie stworzenia (all wszystkie , first pierwsze)
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Ceneo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error :("

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Ceneo.query.get_or_404(id)

    if request.method == 'POST':
        task.author_name = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating :("
    else:
        return render_template('update.html',task = task)


if __name__ == "__main__":
    app.run(debug = True)