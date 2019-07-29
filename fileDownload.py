from flask_restful import Resource
from flask import request, Response
from resources import get_bucket, get_buckets_list
from models.eventLog import LogModel

class FileDownload(Resource):
    def post(self):
        key = request.form['key']

        my_bucket = get_bucket()
        file_obj = my_bucket.Object(key).get()
        event_log = LogModel('download_event', key)
        try:
            event_log.save_to_db()
        except:
            return {"message": "An error occurred while logging."}, 500

        return Response(
            file_obj['Body'].read(),
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename={}".format(key)}
        )