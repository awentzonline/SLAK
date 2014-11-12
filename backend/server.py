from gevent.monkey import patch_all; patch_all()

import time

import gevent
import redis
import uwsgi


client_id = 0
last_message_t = {}


def application(env, sr):
    global client_id
    client_id += 1
    this_client = client_id

    uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
    print("websockets...")
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    channel = r.pubsub()
    channel.subscribe('foobar')

    websocket_fd = uwsgi.connection_fd()
    redis_fd = channel.connection._sock.fileno()
    
    while True:
        ready = gevent.select.select([websocket_fd, redis_fd], [], [], 3.0)
        if not ready[0]:
            uwsgi.websocket_recv_nb()
        for fd in ready[0]:
            if fd == websocket_fd:
                msg = uwsgi.websocket_recv_nb()
                if msg:
                    # rate limit messages
                    last_time = last_message_t.get(client_id)
                    now = time.time()
                    if last_time:
                        dt = now - last_time
                        if dt < 0.5:
                            continue
                    last_message_t[client_id] = now
                    r.publish('foobar', msg)
            elif fd == redis_fd:
                msg = channel.parse_response() 
                # only interested in user messages
                if msg[0] == 'message':
                    uwsgi.websocket_send("[%s] %s" % (time.time(), msg[2]))





