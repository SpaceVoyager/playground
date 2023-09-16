import redis

r = redis.StrictRedis(host='newpi4.local', port=6379)

r.set('mykey', 'Hello from Python!')
value = r.get('mykey')
print(value)

r.zadd('leaderboard', {'Luke' : 5563})
r.zadd('leaderboard', {'Yuhang' : 800})
leaderboard = r.zrange('leaderboard', 0, -1, withscores=True)
print(leaderboard)

r.connection_pool.disconnect()
