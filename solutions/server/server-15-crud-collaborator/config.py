# This file contains the configuration variables that your app needs.

VERSION = 15.0
HOST    = 'localhost'
PORT    = 20015

SECRET = 'mostly awesome'

# This is the path to the upload directory
UPLOAD_FOLDER = 'uploads/'
# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = ['txt', 'md', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif']

# Should the database be reinitialized each time the server is restarted?
DB_SEED = False
