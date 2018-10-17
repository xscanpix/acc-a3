from celery import Celery
from flask import Flask

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def print_hello():
    return 'hello there'

@celery.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results

@app.route('/prime', methods=['GET'])
def prime():
	return gen_prime(100)

@app.route('/hello', methods=['GET'])
def hello():
	return print_hello()

if __name__ == '__main__':
	app.run(debug=True)