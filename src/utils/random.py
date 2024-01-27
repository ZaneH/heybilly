import base64
import os


def random_id():
    return base64.b64encode(os.urandom(32))[:8].decode('utf-8')
