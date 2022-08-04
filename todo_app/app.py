from flask import Flask, render_template, redirect, request, url_for
from todo_app.data.trello_items import TrelloItems
from todo_app.data.view_model import ViewModel

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trello_items = TrelloItems()

    @app.route('/')
    def index():
        items = trello_items.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add', methods = ['POST'])
    def add_new_item():
        title = request.form['title']
        trello_items.add_item(title)
        return redirect(url_for('index'))

    @app.route('/change-status/<id>', methods = ['POST'])
    def move_item(id):
        trello_items.change_status(id)
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app()
