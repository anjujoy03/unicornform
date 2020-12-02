import json
import datetime
import decimal
import numpy as np
from collections import OrderedDict
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta

Base = declarative_base()

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        print(obj)
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                # if field == 'tran_amt':
                print("data === " , data)
                try:
                    #if data != None and data != 0:
                    if isinstance(data, decimal.Decimal):
                        fields[field] = data.__str__()
                    elif isinstance(data, datetime.datetime):
                        fields[field] = data.__str__()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.__str__()
                    else:
                        json.dumps(data) # this will fail on non-encodable values, like other classes
                        fields[field] = data.__str__()

                except TypeError:
                    pass
                    # print(TypeError)
            # a json-encodable dict
            # print(fields)
                return fields
            return json.JSONEncoder.default(self, obj)

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray,)): #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
