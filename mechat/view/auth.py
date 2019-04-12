from flask import Blueprint, request

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=["GET", "POST"])
def loing():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == 'root' and password == 'toor':
            return
