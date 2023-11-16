#!/usr/bin/env python3
'''
Basic Flask app
'''

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app: Flask = Flask(__name__)

AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> dict:
    ''' GET /
    Return:
      - JSON payload
    '''
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> dict:
    ''' POST /users
    JSON body:
      - email
      - password
    Return:
      - JSON payload
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": str(err)}), 400
    
@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> dict:
    ''' POST /sessions
    JSON body:
      - email
      - password
    Return:
      - JSON payload
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
