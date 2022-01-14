from flask import Flask, render_template, redirect, request, url_for
from todo_app.data.trello_items import get_cards, add_card, change_status

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_cards()
    return render_template('index.html', items = items)

@app.route('/add', methods = ['POST'])
def add_new_item():
    title = request.form['title']
    add_card(title)
    return redirect(url_for('index'))

@app.route('/change-status/<id>', methods = ['POST'])
def move_item(id):
    change_status(id)
    return redirect(url_for('index'))
