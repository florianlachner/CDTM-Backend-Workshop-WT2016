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
    # TODO: compute right path
    directory =
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the name of the uploaded files
    uploaded_files = request.files.getlist('files[]')
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            # sanitize the filename
            filename = secure_filename(file.filename)
            # TODO: save uploaded file permanently
            # TODO: save reference in database


    # TODO: return the updated task
    task =
    if task == None:
        json_abort(500, 'Could not upload file')

    return jsonify(task.__dict__)
