from utils import *
from server import app

def db_get_collaborators_for_list(list_id):
    ''' Returns a list of all collaborators for a list from the database '''
    query = '''
        SELECT user_id
        FROM Collaborators
        WHERE list_id = ?;
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [list_id])
        db.commit()
        return [dict_from_row(row)['user_id'] for row in cur]


def db_add_collaborator(list_id, user_id):
    ''' adds a new collaborator '''

    query = '''
        INSERT OR REPLACE
        INTO Collaborators(list_id, user_id)
        Values (?, ?);
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [list_id, user_id])
        db.commit()


def db_remove_collaborator(list_id, user_id):
    ''' deletes a collaborator from a list '''
    query = '''
        DELETE
        FROM Collaborators
        WHERE list_id = ? AND user_id = ?;
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [list_id, user_id])
        db.commit()
