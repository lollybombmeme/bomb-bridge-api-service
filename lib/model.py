# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from bson import ObjectId, json_util
import datetime as dt

from pydash import get
from pymodm import fields, connection, MongoModel

from .constants import PAGE_SIZE_DEFAULT
# from .decorators.redis import redis_cluster
from .utils import dt_utcnow, is_oid


def get_default(default):
    if callable(default):
        return default()
    return default


def to_str(x):
    if isinstance(x, ObjectId):
        return str(x)
    if not isinstance(x, str):
        return json_util.dumps(x)
    return x


class BaseMG(MongoModel):
    created_by = fields.CharField(default='', blank=True)
    updated_by = fields.CharField(default='', blank=True)
    created_time = fields.DateTimeField(default=None)
    updated_time = fields.DateTimeField(default=None)
    deleted = fields.BooleanField(default=False, blank=True)
    deleted_time = fields.DateTimeField(default=None, blank=True)

    def to_dict(self):
        return self.to_son().to_dict()

    @classmethod
    def bulk(cls, items):
        _rows = [cls(**cls.init_row(row)) for row in items]
        if _rows:
            return cls.objects.bulk_create(_rows)
        return False

    @classmethod
    def db(cls):
        return connection._get_db(cls._mongometa.connection_alias)[cls._mongometa.collection_name]

    @classmethod
    def init_row(cls, payload):
        _init = {}
        for field in cls._mongometa.get_fields():
            if field.mongo_name == '_id':
                if not isinstance(payload.get('_id'), ObjectId):
                    if is_oid(payload.get(field.mongo_name)):
                        _init[field.mongo_name] = ObjectId(payload.get(field.mongo_name))
                    else:
                        _init[field.mongo_name] = ObjectId()
            else:
                if field.mongo_name in ['created_time', 'updated_time']:
                    if not isinstance(field.mongo_name, dt.datetime):
                        if isinstance(field.mongo_name, (float, int)):
                            _init[field.mongo_name] = dt.datetime.fromtimestamp(
                                payload.get(field.mongo_name, get_default(field.default)))
                        else:
                            _init[field.mongo_name] = dt_utcnow()
                    else:
                        _init[field.mongo_name] = payload.get(field.mongo_name, get_default(field.default))
                else:
                    _init[field.mongo_name] = payload.get(field.mongo_name, get_default(field.default))
        return _init

    @classmethod
    def insert(cls, obj):
        return cls(**cls.init_row(obj)).save()

    @classmethod
    def update_one(cls, filter, obj, upsert=False):
        if not isinstance(obj, dict):
            raise TypeError("obj must be dictionary!")

        obj["updated_time"] = dt_utcnow()
        return cls.db().update_one(filter, {"$set": obj}, upsert=upsert)

    @classmethod
    def update_raw(cls, filter, raw_obj, upsert=False):
        if not isinstance(raw_obj, dict):
            raise TypeError("obj must be dictionary!")

        if "$set" in raw_obj:
            raw_obj["$set"]["updated_time"] = dt_utcnow()
        else:
            raw_obj["$set"] = {"updated_time": dt_utcnow()}

        print(filter, raw_obj)
        return cls.db().update(filter, raw_obj, upsert=upsert)

    @classmethod
    def update_by_filter(cls, filter, obj, upsert=False, multi=False):
        obj["updated_time"] = dt_utcnow()
        return cls.db().update(filter, {"$set": obj}, upsert=upsert, multi=multi)

    @classmethod
    def delete(cls, oid, force=False):
        if ObjectId.is_valid(oid):
            oid = ObjectId(oid)

        if force:
            return cls.db().delete_one({"_id": oid})

        return cls.update(oid, {"deleted": True, 'deleted_time': dt_utcnow()})

    @classmethod
    def get_public_address(cls, public_address, is_one=False, page=1, page_size=PAGE_SIZE_DEFAULT):
        if is_one:
            return cls.db().find_one({"public_address": public_address})
        else:
            return cls.db().find({"public_address": public_address}).sort('_id', -1).skip(
                int((page - 1) * page_size)).limit(page_size)

    @classmethod
    def get_item(cls, oid):
        if ObjectId.is_valid(oid):
            oid = ObjectId(oid)

        return cls.db().find_one({"_id": oid})

    @classmethod
    def get_item_with(cls, filter):
        return cls.db().find_one(filter)

    @classmethod
    def get_list(cls, filter: dict = {}, sort=[], page: int = 1, page_size: int = PAGE_SIZE_DEFAULT) -> list:
        if not page:
            page = 1

        if not sort:
            sort = [("_id", -1)]

        return cls.db().find(filter).sort(sort).skip(int((page - 1) * page_size)).limit(page_size)

    @classmethod
    def get_count(cls, filter={}):
        return cls.db().find(filter).count()

    @classmethod
    def get_random_items(cls, filter={}, sort={}, size=1):
        if sort:
            return cls.db().aggregate([
                {"$match": filter},
                {"$sort": sort},
                {"$sample": {"size": size}}
            ])

        return cls.db().aggregate([
            {"$match": filter},
            {"$sample": {"size": size}}
        ])

    @classmethod
    def aggregate(cls, pipelines):
        return cls.db().aggregate(pipelines)

    @classmethod
    def get_obj_form_dict(cls, data: dict):
        _obj = {}
        for field in cls._mongometa.get_fields():
            if data.get(field.mongo_name):
                _obj[field.mongo_name] = data.get(field.mongo_name)
        return _obj

    @classmethod
    def find(cls, filter: dict, with_cache: bool = True, field_key='_id', *args, **kwargs) -> list:
        """
        Run script: python3 sync/collection.py db=<db name> col=<collection name> key_sync=<list keys form filter> type=<field_key> tll=-1
        EX:
            Run:  python3 sync/collection.py db=dapp col=nft key_sync=on_market#true type=_id  tll=-1

            Model.find(filter={"on_market": True}, field_key='_id')

        :param filter:
        :param with_cache:
        :param field_key: field of hset
        :param args:
        :param kwargs:
        :return: list
        """
        _filter_keys = list(filter.keys())

        _filter_keys.sort()

        _fields = [f'{x}:{to_str(filter[x])}' for x in _filter_keys]

        _key = f'{cls._mongometa.connection_alias}:{cls._mongometa.collection_name}:{"".join(_fields)}'

        def query():
            return list(cls.db().find(filter=filter, *args, **kwargs))

        # if with_cache:
        #     _raws = redis_cluster.hvals(_key)
        #     if _raws is not None:
        #         return [json_util.loads(_raw) for _raw in _raws]
        #     _raws = query()
        #     if _raws:
        #         for _raw in _raws:
        #             redis_cluster.hset(_key, to_str(get(_raw, field_key)), json_util.dumps(_raw))
        #     return _raws

        return query()

    @classmethod
    def find_one(cls, filter: dict, with_cache: bool = True, *args, **kwargs):
        """
        Run script: python3 sync/collection.py db=<db name> col=<collection name> key_sync=<list keys form filter> tll=-1
        Ex:
            Run: python3 sync/collection.py db=dapp col=users key_sync=public_address tll=-1
            Model.find_one({"public_address": "...."})

        :param filter:
        :param with_cache:
        :param args:
        :param kwargs:
        :return:
        """

        _filter_keys = list(filter.keys())

        _filter_keys.sort()

        _fields = [f'{x}:{to_str(filter[x])}' for x in _filter_keys]

        _key = f'{cls._mongometa.connection_alias}:{cls._mongometa.collection_name}:{"".join(_fields)}'

        def query():
            return cls.db().find_one(filter=filter, *args, **kwargs)

        # if with_cache:
        #     _raw = redis_cluster.get(_key)
        #     if _raw is not None:
        #         return json_util.loads(_raw)
        #     _raw = query()
        #     if _raw:
        #         redis_cluster.set(_key, json_util.dumps(_raw))
        #     return _raw

        return query()

    @classmethod
    def page(cls, filter, page_size: int, page: int, sort=1, func_sort=None, func_filter=None, field_key='_id'):
        _list = cls.find(filter=filter, field_key=field_key)
        if func_filter:
            _list = [x for x in _list if func_filter(x)]
        if func_sort:
            if sort == 1:
                _list.sort(key=func_sort)
            else:
                _list.sort(key=func_sort, reverse=True)
        _offset = page_size * (page - 1)
        _limit = (int(page * page_size))
        _offset = int(_limit - page_size)
        result = _list[_offset:_limit]
        num_of_page = (len(_list) / page_size)
        if (len(_list) % page_size) > 0:
            num_of_page = num_of_page + 1

        return {
            "items": result,
            'num_of_page': num_of_page,
            'page_size': page_size,
            'page': page
        }
