from flask.json import JSONEncoder
from datetime import datetime as dt

from server.util.instances import db


class JSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return obj.json()

        if isinstance(obj, dt):
            #return o.strftime("%Y-%m-%d %H:%M:%S")
            return obj.strftime("%d-%m-%Y")

        return JSONEncoder.default(self, obj)