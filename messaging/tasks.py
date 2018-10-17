from celery import Celery
from flask import Flask

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost:5000/0'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://localhost:5000/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app = Celery('tasks', backend='amqp', broker='amqp://localhost:5000/0')

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