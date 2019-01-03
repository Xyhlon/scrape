# from bson.binary import Binary
from datetime import datetime, timedelta

from pymongo import MongoClient, errors


# import zlib


class MongoCache:
    DONE, DOING, WAITING = range(3)

    def __init__(self, client=None, delay=300, expires=timedelta(days=30)):
        self.client = MongoClient('localhost', 27017, connect=False) if client is None else client
        self.db = self.client.cache
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())
        self.delay = delay
        # print(self.client.list_database_names())
        # print(self.client.cache)

    def __setitem__(self, key, value):
        ref = {'result': value, 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': key}, {'$set': ref}, upsert=True)
        # maybe compress ref

    def __getitem__(self, item):
        ref = self.db.webpage.find_one({'_id': item})
        if ref:
            return ref['result']
            # zlib.decompress(ref['result'])
        else:
            raise KeyError(item + "isn't in cache")

    def __contains__(self, item):
        try:
            self[item]
        except KeyError:
            return False
        else:
            return True

    def clear(self):
        self.db.webpage.drop()
        self.db.queue.drop()

    def __nonzero__(self):
        ref = self.db.queue.find_one({'status': {'$P': self.DONE}})
        return True if ref else False

    def push(self, url):
        try:
            self.db.queue.insert({'_id': url, 'status': self.WAITING})
            # print(url + ' is new')
        except errors.DuplicateKeyError as E:
            # maybe print url and say it is already in queue
            # print(url + ' already exists')
            pass

    def pop(self):
        ref = self.db.queue.find_and_modify(query={'status': self.WAITING},
                                            update={'$set': {'status': self.DOING, 'timestamp': datetime.now()}})
        if ref:
            return ref['_id']
        else:
            self.repair()
            raise KeyError()

    def done(self, url):
        self.db.queue.update({'_id': url}, {'$set': {'status': self.DONE}})
        # print(url + ' is done')

    def check(self):
        ref = self.db.queue.find_one({'status': self.WAITING})
        if ref:
            return ref['_id']

    def repair(self):
        ref = self.db.queue.find_and_modify(
            query={'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.delay)}, 'status': {'$ne': self.DONE}},
            update={'$set': {'status': self.WAITING}})
        if ref:
            print('Released:' + ref['_id'])

    def status(self):
        for stuff in self.db.queue.find():
            print(stuff)

    def still(self):
        if self.db.queue.find_one({'status': self.WAITING}):
            return True
