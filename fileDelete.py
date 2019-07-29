from flask_restful import Resource
from flask import request, flash, redirect, url_for
from resources import get_bucket
from models.eventLog import LogModel

class FileDelete(Resource):
    def post(self):
        key = request.form['key']

        my_bucket = get_bucket()
        my_bucket.Object(key).delete()

        flash('File deleted successfully')
        event_log = LogModel('delete_event', key)
        try:
            event_log.save_to_db()
        except:
            return {"message": "An error occurred while logging."}, 500
        return redirect(url_for('files'))