from datetime import timedelta

BROKER_URL = 'redis://localhost:6379/0'

CELERYBEAT_SCHEDULE = {
    'activeate-pump': {
        'task': 'tasks.pump',
        'schedule': timedelta(seconds=1800),
    },
    'read-photoresistor': {
        'task': 'tasks.photoresistor',
        'schedule': timedelta(seconds=30),
    },
}

