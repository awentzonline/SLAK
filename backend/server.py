from gevent.monkey import patch_all; patch_all()

import time

import gevent
import redis
import uwsgi

from tremolo import TremoloApp


class SLAKApp(TremoloApp):
    """UTTERLY DISTRUPTIVE CHAT SERVER"""

    def __init__(self, *args, **kwargs):
        super(SLAKApp, self).__init__(*args, **kwargs)
        self.last_message_t = {}

    def setup(self, core_id):
        self.last_message_t[core_id] = 0

    def websocket(self, core_id, msg):
        last_t = self.last_message_t[core_id]
        now = time.time()
        dt = now - last_t
        if dt >= 0.5 or not last_t:
            self.r.publish(self.room, msg)
            self.last_message_t[core_id] = now


application = SLAKApp()
