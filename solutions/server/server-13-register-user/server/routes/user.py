from flask import request, session, jsonify

from server import app
from server.database import *
from server.utils import isEmail, has_json

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
            return jsonify({'result': True, 'text': 'User successfully created'})

    return jsonify({'result': False, 'text': 'User already exists'})
