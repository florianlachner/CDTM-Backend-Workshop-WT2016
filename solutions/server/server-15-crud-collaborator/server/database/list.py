from utils import *

from server import app
from server.models import List
from collaborator import db_get_collaborators_for_list


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

def db_has_access_to_list(list_id, user_id):
  ''' Returns whether a user has access to a certain list'''
  query = '''
      SELECT DISTINCT lists.id AS id
      FROM lists LEFT OUTER JOIN collaborators ON lists.id = collaborators.list_id
      WHERE lists.id = ?
          AND (lists.owner = ? OR collaborators.user_id = ?)
  '''

  with app.app_context():
      cur = get_db().cursor()
      cur.execute(query, [list_id, user_id, user_id])
      result = dict_from_row(cur.fetchone())
      return result.get('id') != None
  return False

def db_is_list_owner(list_id, user_id):
  ''' Returns whether a user owns a certain list'''
  query = '''
      SELECT id
      FROM lists
      WHERE lists.id = ?
          AND lists.owner = ?
  '''

  with app.app_context():
      cur = get_db().cursor()
      cur.execute(query, [list_id, user_id])
      result = dict_from_row(cur.fetchone())
      return result.get('id') != None
  return False

def db_get_lists(user_id):
    ''' Queries the db for all lists'''
    query = '''
      SELECT DISTINCT lists.id, lists.title, lists.owner, lists.revision, lists.inbox
      FROM lists LEFT OUTER JOIN collaborators ON lists.id = collaborators.list_id
      WHERE lists.owner = ? OR collaborators.user_id = ?
    '''

    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [user_id, user_id])
        lists = []
        for row in cur:
            l = List.fromDict(dict_from_row(row))
            if isinstance(l, List):
                l.collaborators = db_get_collaborators_for_list(l.id)
                lists.append(l)
        return lists


def db_get_list(list_id):
    ''' Queries the db for a specific list'''
    query = '''
        SELECT id, title, owner, revision, inbox
        FROM lists
        WHERE id = ?
    '''

    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [list_id])
        l = List.fromDict(dict_from_row(cur.fetchone()))
        if isinstance(l, List):
            l.collaborators = db_get_collaborators_for_list(l.id)
        return l


def db_create_list(title, owner_id, inbox=False):
    ''' Creates a new user, if it does not exist yet'''
    query = '''
        INSERT INTO Lists(title, owner, inbox, revision)
        VALUES (?,?,?,1);
    '''
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [title, owner_id, 1 if inbox else 0])
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
