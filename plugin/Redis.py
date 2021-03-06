# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 12:15:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import sys
import redis
import json
from cottle import handle

name = 'redis'

class index(handle):
    def GET(self):
        return self.template('redis')

class RedisOptions(handle):
    def Before(self):
        host = self.params[0]
        port = self.params[1]
        db   = self.params[2]
        try:
            self.red = redis.Redis(port = port, host = host, db = db)
        except:
            self.abort(500, '%s/%s/%s Error' % (host, port, db))
        return True

    def After(self):
        del self.red

class KEYS(RedisOptions):
    def GET(self):
        return self.red.keys()

class KEYS_KEY(RedisOptions):
    def GET(self):
        red = self.red
        key = self.params[-1]
        t = red.type(key)
        res = {'type': t, 'value': None}
        if t == 'none':
            value = None

        if t == 'hash':
            value = red.hgetall(key)

        if t == 'string':
            value = red.get(key)

        if t == 'set':
            value = red.smembers(key)

        if t == 'list':
            value = red.lrange(key, 0, -1)

        res['value'] = value
        return res


urls = (
        '/', index,
        "/([^/]+)/([^/]+)/([^/]+)/KEYS", KEYS,
        "/([^/]+)/([^/]+)/([^/]+)/KEYS/(.+)", KEYS_KEY,
        )


if __name__ == "__main__":
    pass

