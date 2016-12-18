from flask import jsonify

from src.server.server.database import *

@app.route('/api/lists', methods=['GET'])
def get_lists():
    response = {}
    myLists = db_get_lists()
    response['lists'] = [l.__dict__ for l in myLists]
    return jsonify(response)