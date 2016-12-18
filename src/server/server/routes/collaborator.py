from flask import request, jsonify, session

from server import app
from server.database import *
from server.utils import login_required, list_owner, list_access, json_abort

@app.route('/api/lists/<string:list_id>/collaborators/<string:collaborator_email>', methods=['POST'])
# TODO: Add correct decorators
def add_collaborator(list_id, collaborator_email):
    # TODO: check whether user exists
    user =
    if user == None:
        json_abort(404, 'User not found')

    # TODO: Add collaborator to list
    db_add_collaborator(l.id, user.id)

    # TODO: Get list from database and return it
    l =
    if l == None:
        json_abort(404, "List not updated")

    return jsonify(l.__dict__)


# REMOVE collaborator
@app.route('/api/lists/<string:list_id>/collaborators/<string:collaborator_id>', methods=['DELETE'])
# TODO: Add correct decorators
def remove_collaborator(list_id, collaborator_id):
    # collaborators can only be removed by a list owner, unless a collaborator want to remove himself
    if collaborator_id != str(session.get('userID')):
        if not db_is_list_owner(list_id, session.get('userID')):
            json_abort(404, 'List not found')

    if db_get_user_by_id(collaborator_id) == None:
        json_abort(400, 'Invalid request parameters')

    # TODO: remove collaborator
    
    return jsonify({'result': True})
