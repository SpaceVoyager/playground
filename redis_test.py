import redis

pool = redis.ConnectionPool(host='newpi4.local', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

redis.set('mykey', 'Hello from Python!')
value = redis.get('mykey')
print(value)
redis.zadd('leaderboard', {'Luke' : 5563})
redis.zadd('leaderboard', {'Yuhang' : 800})
leaderboard = redis.zrange('leaderboard', 0, -1, withscores=True)
print(leaderboard)
