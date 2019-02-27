from flask import Flask,render_template,redirect,url_for,request,flash,session,logging,request,abort,g
from passlib.hash import sha256_crypt
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Berk/Desktop/TodoApp/user.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    
    return render_template("index.html")
@app.route("/yayinla/<string:id>")
def completeArticle(id):
    article = Article.query.filter_by(id = id).first()
    article.yayinla = not article.yayinla
    if article.yayinla == True:
        flash('Yayına Alındı...',"success")
    else:
        flash('Yayından Kaldırldı...',"danger")       


    db.session.commit()

    return redirect(url_for("kullanici_paneli"))

@app.route("/delete/<string:id>")
def deleteArticle(id):
    article = Article.query.filter_by(id = id).first()
    db.session.delete(article)
    db.session.commit()

    return redirect(url_for("kullanici_paneli"))


@app.route("/register", methods = ["GET","POST"])
def addUser():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    newUser = User(username = username, email = email, password = password, authenticated = False )
    db.session.add(newUser)
    db.session.commit()
    flash('Başarıyla Kayıt Oldunuz....',"success")           
    return redirect(url_for("index"))
#User Register
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
# Register Page
@app.route("/register")
def register():
    return render_template("register.html")
# Kullanıcı Paneli
@app.route("/kullanici_paneli")
@login_required
def kullanici_paneli():
    articles = Article.query.all()
    return render_template("/kullanici_paneli.html",articles = articles)
# Login Page
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash("Kullanıcı Adı veya Şifreniz Yanlış..." , "danger")
        return redirect(url_for("login"))
    login_user(registered_user)
    flash("Başarıyla Giriş Yaptınız...","success")
    return redirect(request.args.get("next") or url_for("index"))

# Logout Page
@app.route('/logout')
def logout():
    logout_user()
    flash("Başarıyla Çıkış Yaptınız...","success")
    return redirect(url_for('index')) 
@app.route("/article")
def article():
    articles = Article.query.all()
    return render_template("article.html",articles= articles)
# Makale Database
@app.route("/addarticles", methods = ["GET","POST"])
def addArticle():
    if request.method == 'GET':
        return render_template('addarticles.html')
    title = request.form.get("title")
    content = request.form.get("content")
    newArticle= Article(title = title, content = content, yayinla = True )
    db.session.add(newArticle)
    db.session.commit()
    flash('Makaleyi Başarıyla Oluşturdunuz....',"success")           
    return redirect(url_for("article"))
#Article Register
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String)
    article_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    yayinla = db.Column(db.Boolean, default=True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_yayinla(self):
        """Return True if the user is authenticated."""
        return self.yayinla

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)