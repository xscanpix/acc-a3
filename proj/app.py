from flask import Flask
from celery import Celery

CELERY_TASK_LIST = [
    'tasks',
]

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('settings')
app.config.from_pyfile('settings.py', silent=True)

if settings_override:
    app.config.update(settings_override)

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                include=CELERY_TASK_LIST)
celery.conf.update(app.config)
TaskBase = celery.Task

class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask

@app.route('/prime', methods=['GET'])
def prime():
return gen_prime(100)

@app.route('/hello', methods=['GET'])
def hello():
    return print_hello()
