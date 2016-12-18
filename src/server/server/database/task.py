from utils import *

from utils import *

from src.server.server import app
from src.server.server.models import Task


def db_get_tasks_for_list(list_id):
    ''' Returns all tasks from the database for a given list'''
    query = '''
    SELECT * FROM Tasks WHERE list = ?
    '''
    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [list_id])
        tasks = []
        for row in cur:
            task = Task.fromDict(dict_from_row(row))
            if isinstance(task, Task):
                tasks.append(task)
        return tasks

def db_get_task(list_id, task_id):
    ''' Queries the db for a task with the specified id'''
    query = '''
    SELECT * FROM Tasks WHERE list = ? AND id = ?
    '''

    with app.app_context():
        cur = get_db().cursor()
        cur.execute(query, [task_id, list_id])
        task = Task.fromDict(dict_from_row(cur.fetchone()))
        return task


def db_create_task(list_id, title):
    ''' Inserts a new task and returns it '''
    query = '''
    INSERT INTO Tasks (title, list, status) VALUES (?, ?, 'normal')
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [title, list_id])
        db.commit()

    return db_get_task(list_id, cur.lastrowid)

def db_update_task(list_id, task):
    ''' Updates a task and returns it '''
    query = '''
    UPDATE Tasks SET (title, list, status, description, due, revision) VALUES (?, ?, ?, ?, ?, ?)
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [task.title, task.list, task.status, task.description, task.due, task.revision, task.id])
        db.commit()

    return db_get_task(list_id, task.id)

def db_delete_task(id):
    ''' Deletes the task with the specified id '''
    query = '''
    DELETE FROM Tasks WHERE id = ?
    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [id])
        db.commit()
