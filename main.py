from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)

@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/index')
            else:
                error = 'Nombre de usuario o contraseña incorrectos'
            return render_template('login.html', error=error)
        else:
            return render_template('login.html')

@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        #Tarea 3
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:    
        return render_template('registration.html')

@app.route('/index')
def index():
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    return render_template('card.html', card=card)

@app.route('/create')
def create():
    return render_template('create_card.html')

@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')
    
#Crea la ruta /voice

if __name__ == "__main__":
    app.run(debug=True)
