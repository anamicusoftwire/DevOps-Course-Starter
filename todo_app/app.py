import os
from flask import Flask, render_template, redirect, request, url_for
from todo_app.data.authorization import get_identity, get_user_details
from todo_app.data.trello_items import TrelloItems
from todo_app.data.user import User
from todo_app.data.view_model import ViewModel
from flask_login import LoginManager, login_required, login_user
from loggly.handlers import HTTPSHandler
from logging import Formatter

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    loggly_token = os.environ.get('LOGGLY_TOKEN')


    if loggly_token is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{loggly_token}/tag/todo-app')
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(handler)

    trello_items = TrelloItems(app.logger)

    @app.route('/')
    @login_required
    def index():
        items = trello_items.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add', methods = ['POST'])
    @login_required
    def add_new_item():
        title = request.form['title']
        trello_items.add_item(title)
        return redirect(url_for('index'))

    @app.route('/change-status/<id>', methods = ['POST'])
    @login_required
    def move_item(id):
        trello_items.change_status(id)
        return redirect(url_for('index'))

    @app.route('/login/callback')
    def login_callback():
        code = request.args.get('code')
        user = get_user_details(code)
        login_user(user)
        app.logger.info("User %s was logged in.", user.id)

        return redirect(url_for('index'))

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        return get_identity()

    unauthenticated
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    return app

if __name__ == '__main__':
    create_app()
