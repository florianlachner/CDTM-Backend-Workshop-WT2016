from utils import *

from server import app
from server.models import List


def db_list_exists(list_id):
    ''' Returns whether a certain list exists'''
    query = '''
        SELECT DISTINCT lists.id AS id
        FROM lists
        WHERE lists.id = ?
    '''
    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [list_id])
        result = dict_from_row(cur.fetchone())
        return result.get('id') != None
    return False


def db_get_lists():
    ''' Queries the db for all lists'''
    query = '''
        SELECT DISTINCT lists.id, lists.title, lists.revision, lists.inbox
        FROM lists
    '''

    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [])
        lists = []
        for row in cur:
            l = List.fromDict(dict_from_row(row))
            if isinstance(l, List):
                lists.append(l)
        return lists


def db_get_list(list_id):
    ''' Queries the db for a specific list'''
    query = '''
        SELECT id, title, revision, inbox
        FROM lists
        WHERE id = ?
    '''

    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [list_id])
        l = List.fromDict(dict_from_row(cur.fetchone()))
        return l


def db_create_list(title, inbox=False):
    ''' Creates a new user, if it does not exist yet'''
    query = '''
        INSERT INTO Lists(title, inbox, revision)
        VALUES (?,?,1);
    '''
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [title, 1 if inbox else 0])
        db.commit()
        return db_get_list(cur.lastrowid)


def db_update_list(l):
    ''' Updates a list and returns it '''
    query = '''
        UPDATE lists
        SET title = ?, revision = ?
        WHERE id = ?;
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [l.title, l.revision, l.id])
        db.commit()

    return db_get_list(l.id)


def db_delete_list(id):
    ''' Deletes the list and all it's tasks with the specified id '''
    query = '''
        DELETE FROM lists WHERE id = ?;
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [id])
        db.commit()
