from flask import request, jsonify, send_from_directory
from werkzeug import secure_filename

import os, shutil

from server import app
from server.database import *
from server.utils import allowed_file, list_exists, json_abort

# UPLOAD FILES
@app.route('/api/lists/<string:list_id>/tasks/<string:task_id>/files', methods=['POST'])
@list_exists
def upload_file(list_id, task_id):
    # each file is save in a folder named after the corresponding tasks id and list_id
    directory = os.path.join(app.config['UPLOAD_FOLDER'], list_id, task_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the name of the uploaded files
    uploaded_files = request.files.getlist('files[]')
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            # sanitize the filename
            filename = secure_filename(file.filename)
            # save uploaded file permanently
            file.save(os.path.join(directory, filename))
            # save reference in database
            db_create_file(task_id, filename)

    # return the updated task
    task = db_get_task(list_id, task_id)
    if task == None:
        json_abort(500, 'Could not upload file')

    return jsonify(task.__dict__)

# GET FILE
@app.route('/api/lists/<string:list_id>/tasks/<string:task_id>/files/<string:filename>', methods=['GET'])
@list_exists
def get_file(list_id, task_id, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], list_id, task_id)
    return send_from_directory(directory, filename)


# REMOVE FILE
@app.route('/api/lists/<string:list_id>/tasks/<string:task_id>/files/<string:filename>', methods=['DELETE'])
@list_exists
def remove_file(list_id, task_id, filename):
    db_delete_file(task_id, filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], list_id, task_id, filename)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)
    return jsonify({'result': True})
