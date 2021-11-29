from flask import Flask, render_template, redirect, request, url_for
from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items = items)

@app.route('/add', methods = ['POST'])
def add_new_item():
    title = request.form['title']
    add_item(title)
    return redirect(url_for('index'))
