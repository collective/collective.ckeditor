import transaction
from OFS.Folder import manage_addFolder
from Products.Transience.Transience import constructTransientObjectContainer


def setup(event):
    db = event.database
    conn = db.open()
    try:
        root = conn.root()
        app = root["Application"]
        tr = transaction.begin()
        try:
            if setup_temp_folder(app):
                tr.note('setup temp_folder collective.ckeditor')
                tr.commit()
        finally:
            tr.abort()
    finally:
        conn.close()


def setup_temp_folder(app):
    added = False
    if 'temp_folder' not in app.objectIds():
        manage_addFolder(app, 'temp_folder')
        added = True
    temp_folder = app['temp_folder']
    if 'session_data' not in temp_folder.objectIds():
        constructTransientObjectContainer(temp_folder, 'session_data')
        added = True
    return added
