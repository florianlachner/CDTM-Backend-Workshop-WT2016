from flask import request, jsonify, session

from server import app
from server.database import *
from server.utils import login_required, list_owner, list_access, json_abort

@app.route('/api/lists/<string:list_id>/collaborators/<string:collaborator_email>', methods=['POST'])
@login_required
@list_owner
def add_collaborator(list_id, collaborator_email):
    user = db_get_user(collaborator_email)
    if user == None:
        json_abort(404, 'User not found')

    l = db_get_list(list_id)
    if l == None:
        json_abort(404, 'List not found')

    db_add_collaborator(l.id, user.id)
    l = db_get_list(l.id)
    if l == None:
        json_abort(404, "List not found")

    return jsonify(l.__dict__), 201


# REMOVE collaborator
@app.route('/api/lists/<string:list_id>/collaborators/<string:collaborator_id>', methods=['DELETE'])
@login_required
@list_access
def remove_collaborator(list_id, collaborator_id):
    if collaborator_id != str(session.get('userID')):
        if not db_is_list_owner(list_id, session.get('userID')):
            json_abort(404, 'List not found')

    if db_get_user_by_id(collaborator_id) == None:
        json_abort(400, 'Invalid request parameters')

    db_remove_collaborator(list_id, collaborator_id)
    return jsonify({'result': True})
