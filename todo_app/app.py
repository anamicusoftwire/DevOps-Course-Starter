from flask import Flask, render_template, redirect, request, url_for
from todo_app.data.trello_items import get_items, add_item, change_status
from todo_app.data.view_model import ViewModel

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    item_view_model = ViewModel(items)
    return render_template('index.html', view_model = item_view_model)

@app.route('/add', methods = ['POST'])
def add_new_item():
    title = request.form['title']
    add_item(title)
    return redirect(url_for('index'))

@app.route('/change-status/<id>', methods = ['POST'])
def move_item(id):
    change_status(id)
    return redirect(url_for('index'))
