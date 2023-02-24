from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' %self.id


# def create_app():
#     app = Flask(__name__)
#
#     with app.app_context():
#         db.create_all()
#
#     return app


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post")
def post():
    articles = Article.query.order_by(Article.date).all()
    return render_template("post.html", articles=articles)


@app.route("/create-article", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "When you add article happen error"

    else:
        return render_template("create-article.html")



# @app.route("/user/<string:name>/<int:id>")
# def user(name, id):
#     return f"User page: {name} - {id}"


@app.route("/start/")
def start():
    return "Start page"

if __name__ == '__main__':
    app.run(debug=True)
