from flask import request, jsonify

from server import app
from server.database import *
from server.utils import json_abort, list_exists, has_json
from server.models import *

# MARK: Task routes
@app.route('/api/lists/<string:list_id>/tasks', methods=['GET'])
@list_exists
def get_tasks(list_id):
    response = {}
    response['tasks'] = [t.__dict__ for t in db_get_tasks_for_list(list_id)]
    return jsonify(response)

# CREATE ROUTE
@app.route('/api/lists/<string:list_id>/tasks', methods=['POST'])
@list_exists
@has_json
def create_task(list_id):
    ''' creates a new task for a list '''
    data = request.get_json()

    title = data.get('title', None)
    if title == None:
        json_abort(400, 'Invalid request parameters')

    newTask = db_create_task(list_id, title)

    if newTask == None:
        json_abort(400, 'Could not create task')

    return jsonify(newTask.__dict__)

# DESTROY ROUTE
@app.route('/api/lists/<string:list_id>/tasks/<string:task_id>', methods=['DELETE'])
@list_exists
def remove_task(list_id, task_id):
    db_delete_task(task_id)
    return jsonify({'result': True})

# UPDATE ROUTE
@app.route('/api/lists/<string:list_id>/tasks/<string:task_id>', methods=['PUT'])
@list_exists
@has_json
def update_task(list_id, task_id):
    data = request.get_json()
    task = db_get_task(list_id, task_id)

    if task == None:
        json_abort(404, 'Task not found')

    title = data.get('title', None)
    status = data.get('status', None)
    description = data.get('description', None)
    due = data.get('due', None)
    revision = data.get('revision', None)

    if title == None or status == None or description == None or \
    revision == None:
        json_abort(400, 'Invalid request parameters')

    # Only update tasks with there is no newer version on the server
    if revision < task.revision:
        json_abort(409, 'Newer version of task available')

    task.title = title
    task.status = status
    task.description = description
    task.due = due
    task.revision = task.revision + 1

    task = db_update_task(list_id, task)
    if task == None:
        json_abort(500, 'Could not update task')

    return jsonify(task.__dict__)
