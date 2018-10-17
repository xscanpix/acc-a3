from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Celery('tasks', backend='amqp', broker='amqp://')

from flask import Flask

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp://'
)
celery = make_celery(flask_app)

@celery.task()
def add_together(a, b):
    return a + b

@app.task(ignore_result=True)
def print_hello():
    print 'hello there'

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
	if i not in multiples:
	    results.append(i)
	    for j in xrange(i*i, x+1, i):
		multiples.append(j)
    return results
