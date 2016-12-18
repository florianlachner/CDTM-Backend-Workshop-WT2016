import os

from server import *
from server.database import *
import config

def init_app():
    if config.DB_SEED:
        init_db()
    elif not os.path.isfile('task.db'):
        init_db()

    app.config['VERSION'] = config.VERSION

    app.config['UPLOAD_FOLDER'] =  os.path.join(app.root_path, '..', config.UPLOAD_FOLDER)
    app.config['ALLOWED_EXTENSIONS'] = set(config.ALLOWED_EXTENSIONS)

if __name__ == '__main__':
    init_app()
    app.run(host=config.HOST, port=config.PORT, debug=True)
