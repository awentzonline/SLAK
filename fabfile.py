from fabric.api import *  # noqa
from fabric.decorators import hosts


env.user = "www-data"
env["disable_known_hosts"] = True


@hosts(['gws.local'])
def restart():
    run("touch /etc/uwsgi-emperor/vassals/gws.ini")