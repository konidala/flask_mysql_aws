from flask_restful import Resource
from flask import request, Response, flash, redirect, url_for
from resources import get_bucket, get_buckets_list, get_all_objects_from_bucket
from models.eventLog import LogModel

class FileUpload(Resource):
    def post(self):
        file = request.files['file']
        files_list = get_all_objects_from_bucket()
        if file.filename in files_list:
            flash('File upload cannot happen due to duplicate file name')
            return redirect(url_for('files'))

        my_bucket = get_bucket()
        my_bucket.Object(file.filename).put(Body=file)

        flash('File uploaded successfully')

        event_log = LogModel('upload_event', file.filename)
        try:
            event_log.save_to_db()
        except:
            return {"message": "An error occurred while logging."}, 500

        return redirect(url_for('files'))