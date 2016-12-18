from flask import jsonify, request

import os, shutil

from server import app
from server.database import *
from server.utils import list_exists, has_json

# MARK: List routes
@app.route('/api/lists', methods=['GET'])
def get_lists():
    response = {}
    response['lists'] = [l.__dict__ for l in db_get_lists()]
    return jsonify(response)


@app.route('/api/lists/<string:list_id>', methods=['GET'])
@list_exists
def get_list(list_id):
    ''' returns the specified list'''
    l = db_get_list(list_id)
    if l == None:
        json_abort(404, "List not found")
    return jsonify(l.__dict__)


@app.route('/api/lists/', methods=['POST'])
@has_json
def create_list():
    ''' creates a new list '''
    data = request.get_json()
    title = data.get('title')

    newList = db_create_list(title)
    if newList == None:
        json_abort(500, 'Could not create list')

    return jsonify(newList.__dict__), 201


@app.route('/api/lists/<string:list_id>', methods=['PUT'])
@list_exists
@has_json
def update_list(list_id):
    l = db_get_list(list_id)
    data = request.get_json()

    #Only update if revision is smaller on the server
    if data.get('revision') != None and data.get('revision') < l.revision:
        json_abort(409, 'Newer version of list available')

    l.title = (data.get('title'))
    l.revision = l.revision + 1

    l = db_update_list(l)
    if l == None:
        json_abort(500, 'Could not update list')

    return jsonify(l.__dict__)


@app.route('/api/lists/<string:list_id>', methods=['DELETE'])
def remove_list(list_id):
    db_delete_list(list_id)

    # delete upload file directory
    directory = os.path.join(app.config['UPLOAD_FOLDER'], list_id)
    shutil.rmtree(directory, ignore_errors=True)

    return jsonify({'result': True})
