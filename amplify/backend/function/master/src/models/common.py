from flask_jwt_extended import get_jwt_identity
from models.constants import TimeFormats
from datetime import datetime, date
from pymongo.cursor import Cursor
from bson import ObjectId
import pytz


class Common:
    def __init__(self):
        self.cache = {}

    @staticmethod
    def get_identity() -> str:
        return get_jwt_identity()

    @staticmethod
    def get_current_utc_time() -> datetime:
        return datetime.now(pytz.utc)

    @staticmethod
    def jsonify(doc: dict) -> dict:
        if not doc or isinstance(doc, str) or isinstance(doc, int) or isinstance(doc, float):
            return doc
        if isinstance(doc, list):
            return [Common.jsonify(item) for item in doc]
        if isinstance(doc, ObjectId):
            return str(doc)
        for field, value in doc.items():
            if isinstance(value, ObjectId):
                doc[field] = str(value)
            elif isinstance(value, datetime):
                if value.tzinfo is None:
                    value = value.replace(tzinfo=pytz.utc)
                doc[field] = value.strftime(TimeFormats.ANTD_TIME_FORMAT)
            elif isinstance(value, dict):
                doc[field] = Common.jsonify(value)
            elif isinstance(value, list):
                doc[field] = [Common.jsonify(item) for item in value]
        return doc

    @staticmethod
    def string_to_date(doc: dict, field: str) -> date:
        if field in doc and doc[field] is not None and isinstance(doc[field], str):
            try:
                doc[field] = datetime.strptime(
                    doc[field], '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                doc[field] = datetime.now(pytz.utc)
        return doc[field]

    @staticmethod
    def clean_dict(doc: dict, dataClass) -> dict:
        if doc:
            document_fields = set(dataClass.__annotations__.keys())
            doc = {k: v for k, v in doc.items() if k in document_fields}
        return doc

    @staticmethod
    def filter_none_values(data: dict | list) -> dict | list:
        """Recursively remove None values from a dictionary or list."""
        if isinstance(data, dict):
            data = {k: v for k, v in data.items() if v is not None}
            return {k: Common.filter_none_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [Common.filter_none_values(v) for v in data if v is not None]
        else:
            return data

    @staticmethod
    def paginate_cursor(cursor: Cursor, page: int, size: int) -> Cursor:
        offset = (page - 1) * size
        if offset < 0:
            offset = 0
        return cursor.skip(offset).limit(size)

    @staticmethod
    def get_filter_query(filter_field: str, filter_value: str, type: str = 'str') -> dict:
        if filter_field and filter_value:
            if filter_field == '_id':
                type = 'oid'
            if type == 'str':
                return {filter_field: {'$regex': filter_value, '$options': 'i'}}
            elif type == 'int':
                return {filter_field: round(float(filter_value), 2)}
            elif type == 'bool':
                return {filter_field: filter_value.lower() == 'true'}
            elif type == 'oid':
                return {filter_field: ObjectId(filter_value)}
            elif type == 'list':
                return {filter_field: {'$in': filter_value.split(',')}}
        return {}

    @staticmethod
    def filter_falsy_values(data):
        """Recursively filter values from nested dictionaries and lists.  

        For dictionaries, removes keys whose values are None, empty strings,  
        empty lists, empty dictionaries, or 0, then recurses into remaining values.  
        For lists, removes None values and recurses into remaining items.  
        """ 
        if isinstance(data, dict):
            data = {k: v for k, v in data.items() if v is not None and v not in [
                '', [], {}]}
            return {k: Common.filter_falsy_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [Common.filter_falsy_values(v) for v in data if v is not None]
        else:
            return data