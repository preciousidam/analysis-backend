import os
import os.path as op
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from wtforms.validators import ValidationError
from flask_admin.babel import gettext
from server.util.instances import db
from datetime import datetime as dt
import imghdr
from flask import current_app
import cloudinary
import cloudinary.uploader as uploader


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),)
    description = db.Column(db.Text,)
    date = db.Column(db.String(80),)
    file = db.Column(db.String(254))
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return f'{self.title} report'

    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file': f'https://res.cloudinary.com/kblinsurance/raw/upload/v1608312210/{self.file.decode("utf-8")}',
            'date': self.date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }





