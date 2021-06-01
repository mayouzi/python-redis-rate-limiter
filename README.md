# rate limiter with Redis

## Install

```shell
git clone https://github.com/mayouzi/python-redis-rate-limiter.git

cd python-redis-rate-limiter

python setup.py install
```

## Usage

```python
from redis import ConnectionPool
from redis_rate_limiter.rate import RateLimit


redis_pool = ConnectionPool(db=1)

key = "/user/profile"

# QPS 10
rate = RateLimit(resource="_api_qps_", max_requests=10, expire=1, redis_pool=redis_pool)

suc, number = rate.usage(key)

if suc:
    print(f"pass already number: {number}")
else:
    print(f"need wait: {number}")
```
