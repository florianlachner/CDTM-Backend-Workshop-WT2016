from utils import *
from server import app

def db_get_filenames_for_task(task_id):
    ''' Returns a list of all files for a tasks from the database '''
    query = '''

    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [task_id])
        db.commit()
        return [dict_from_row(row)['filename'] for row in cur]

def db_create_file(task_id, filename):
    ''' Inserts a new file '''
    query = '''

    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [task_id, filename])
        db.commit()


def db_delete_file(task_id, filename):
    ''' Deletes the file with the task_id and filename '''
    query = '''

    '''

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(query, [task_id, filename])
        db.commit()
