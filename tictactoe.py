import os

import redis
from cmu_graphics import *

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
MY_CHANNEL = 'player1'
OPPONENT_CHANNEL = 'player1'

if REDIS_PASSWORD is None:
    print('Error: The environment variable REDIS_PASSWORD must be set.')
    exit(1)

app.stepsPerSecond = 2
app.background = 'ghostWhite'

r = redis.Redis(host='redis-a2kids-a2kids.aivencloud.com',
                port=15756,
                password=REDIS_PASSWORD,
                charset="utf-8", decode_responses=True)
sub = r.pubsub()
# Listen to my opponent's channel to get their moves.
sub.subscribe(OPPONENT_CHANNEL)


def onStep():
    message = sub.get_message()
    if message:
        if message['data'] == 'o':
            Image('assets/o.png', randrange(0, 300), randrange(0, 300))
        elif message['data'] == 'x':
            Image('assets/x.png', randrange(0, 300), randrange(0, 300))


def onMousePress(mouseX, mouseY):
    # Publish my move to my channel.
    r.publish(MY_CHANNEL, 'o')


cmu_graphics.run()
