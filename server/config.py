import os

GROUP_SERVER_HOST = os.environ.get(
    'GROUP_SERVER_HOST',
    default='http://127.0.0.1:5001'
)
EVENT_SERVER_HOST = os.environ.get(
    'EVENT_SERVER_HOST',
    default='http://127.0.0.1:5002'
)
IMAGE_SERVER_HOST = os.environ.get(
    'IMAGE_SERVER_HOST',
    default='http://127.0.0.1:5003'
)
