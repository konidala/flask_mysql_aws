from db import db

class LogModel(db.Model):
    __tablename__ = 's3log'

    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(80))
    fileName = db.Column(db.String(150))

    def __init__(self, eventName, fileName):
        self.eventName = eventName
        self.fileName = fileName

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()