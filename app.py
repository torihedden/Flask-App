from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Flask will look for templates in the templates folder.
    return render_template('home_extend.html')

@app.route("/about")
def about():
    return render_template('about_extend.html')
