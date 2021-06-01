from hashlib import sha1
from distutils.version import StrictVersion
from six import string_types

from redis.exceptions import NoScriptError
from redis import Redis, ConnectionPool


SCRIPT = b"""
local current
local limitCount    = tonumber(ARGV[1])
local expireSecond  = tonumber(ARGV[2])
local mKey          = KEYS[1]

local incr = function (key, expire)
    local v = redis.call('INCR', key)
    if v == 1 then
        redis.call("EXPIRE", key, expire)
    end
    return v
end

local yetBeyonds = function (key, maxV, expire)
    local t = tonumber(redis.call("PTTL", key))
    local v
    if t > 0 then
        v = t/1000.0
    else
        v = expire*1.0
    end
        return tostring(v)
end

current = tonumber(redis.call("GET", mKey))
if current then
    if current >= limitCount then
        return (yetBeyonds(mKey, limitCount, expireSecond))
    else
        return (incr(mKey, expireSecond))
    end
else
    return (incr(mKey, expireSecond))
end
"""
SCRIPT_HASH = sha1(SCRIPT).hexdigest()


class RedisVersionNotSupported(Exception):
    """
    Rate Limit depends on Redis’ commands EVALSHA and EVAL which are
    only available since the version 2.6.0 of the database.
    """
    pass


class RateLimit(object):
    """
    This class offers an abstraction of a Rate Limit algorithm implemented on
    top of Redis >= 2.6.0.
    """

    def __init__(self, resource, max_requests, expire=None,
                 redis_pool=ConnectionPool(host='127.0.0.1', port=6379, db=0)):

        self._redis = Redis(connection_pool=redis_pool, decode_responses=True)
        if not self._is_rate_limit_supported():
            raise RedisVersionNotSupported()
        self._resource = resource
        self._max_requests = max_requests
        self._expire = expire or 1

    def _key(self, idf):
        return f"{self._resource}{idf}"

    def _is_rate_limit_supported(self):
        redis_version = self._redis.info()['redis_version']
        is_supported = StrictVersion(redis_version) >= StrictVersion('2.6.0')
        return bool(is_supported)

    def usage(self, idf):
        try:
            result = self._redis.evalsha(
                SCRIPT_HASH, 1, self._key(idf), self._max_requests, self._expire)
        except NoScriptError:
            result = self._redis.eval(
                SCRIPT, 1, self._key(idf), self._max_requests, self._expire)

        if isinstance(result, (string_types, bytes)):
            return False, float(result)

        return True, int(result)
