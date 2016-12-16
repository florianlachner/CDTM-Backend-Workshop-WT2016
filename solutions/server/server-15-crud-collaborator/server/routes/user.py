from flask import request, session, jsonify

from server import app
from server.database import *
from server.utils import isEmail, has_json, login_required

# return session state
@app.route('/api/status', methods=['GET'])
def status():
    if session.get('logged_in'):
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})

# register User
@app.route('/api/register', methods=['POST'])
@has_json
def register():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password')
    if email == None or (not isEmail(email)) or password == None or len(password) < 6:
        return jsonify({'result': False, 'text': 'Invalid username and/or password'})
    if db_create_user(email, password):
        # create default task list for user
        user = db_get_user(email)
        if user != None:
            db_create_list('Inbox', user.id, inbox=True)
            return jsonify({'result': True, 'text': 'User successfully created'})

    return jsonify({'result': False, 'text': 'User already exists'})

# login User
@app.route('/api/login', methods=['POST'])
@has_json
def login():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password')

    user = db_check_password(email, password)
    if user != None:
        session['logged_in'] = True
        session['userID'] = user.id
        session['userEmail'] = user.email
        return jsonify({'result': True})
    return jsonify({'result': False})

# logout User
@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('userID', None)
    session.pop('userEmail', None)
    return jsonify({'result': True})


@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    return jsonify({
        'id': session.get('userID'),
        'email': session.get('userEmail')
    })


@app.route('/api/users/<string:id>', methods=['GET'])
@login_required
def get_user_by_id(id):
    user = db_get_user_by_id(id)
    if user == None:
        json_abort(404, "User not found.")

    return jsonify({
        'id': user.id,
        'email': user.email
    })
