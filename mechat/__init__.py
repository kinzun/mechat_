from flask import Flask

from mechat import chat


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chat.chat_bp)
    return app
