from task import myLists

@app.route('/api/lists', methods=['GET'])
def get_lists():
    response = {}
    response['lists'] = [l.__dict__ for l in myLists]
    return jsonify(response)
