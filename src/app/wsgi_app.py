from gevent import monkey

monkey.patch_all()

from src.app.app import app