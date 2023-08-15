from flask import Flask, render_template,request, flash, redirect, url_for,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
import os
from flask import abort

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database/communal.db')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'upload')
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    objet = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text)

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    blogpte_id = db.Column(db.Integer, db.ForeignKey('blogpte.id'))

class Blogpte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    auteur = db.Column(db.String(50))
    grand_titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    commentaires = db.relationship('Commentaire', backref='blogpte', lazy=True)
    image = db.Column(db.String(100))  # Champ pour le nom du fichier d'image


@app.route("/blogpte", methods=['GET', 'POST'])
def blogpte():
    if request.method == 'POST':
        titre = request.form['titre']
        date_creation = datetime.strptime(request.form['date_creation'], '%Y-%m-%d')
        auteur = request.form['auteur']
        grand_titre = request.form['grand_titre']
        description = request.form['description']
        image = request.files['image']
        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blogpte = Blogpte(titre=titre, date_creation=date_creation, auteur=auteur, grand_titre=grand_titre, description=description, image=filename)
        db.session.add(blogpte)
        db.session.commit()
        return 'Post created successfully!'
    return render_template('admin/blogpte.html')


@app.route('/upload/<filename>')
def upload_image(filename):
    uploads_folder = app.config['UPLOAD_FOLDER']
    return send_from_directory(uploads_folder, filename)


@app.route('/publication')
def aff_liste_pub():
        blogptes = Blogpte.query.order_by(Blogpte.date_creation.desc()).all()
        return render_template('admin/publication.html',  blogptes=blogptes )



@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nom = request.form['nom']
        email = request.form['email']
        objet = request.form["objet"]
        message = request.form['message']
        contact = Contact(nom=nom, email=email, objet=objet, message=message)
        db.session.add(contact)
        db.session.commit()
    return render_template('pages/contact.html')

@app.route("/blog", methods=["GET", "POST"])
def blog():
    if request.method == 'POST':
        message = request.form['message']
        commentaire = Commentaire(message=message)
        db.session.add(commentaire)
        db.session.commit()
    return render_template('pages/blog.html')

@app.route("/")
def page1():
    return render_template('pages/page1.html')

@app.route("/actualite")
def actualite():
    return render_template('pages/actualite.html')

@app.route("/cm")
def cm():
    return render_template('pages/cm.html')

@app.route("/publication")
def publication():
    return render_template('admin/publication.html')

@app.route("/message")
def message():
    return render_template('admin/message.html')

@app.route("/pageadmin")
def pageadmin():
    return render_template('admin/pageadmin.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)


