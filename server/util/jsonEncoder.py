from flask.json import JSONEncoder
from datetime import datetime as dt
import numpy as np

from server.util.instances import db


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return obj.json()

        if isinstance(obj, dt):
            #return o.strftime("%Y-%m-%d %H:%M:%S")
            return obj.strftime("%d-%m-%Y")

        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray,)): #### This is the fix
            return obj.tolist()

        return JSONEncoder.default(self, obj)