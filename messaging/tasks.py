from celery import Celery
from flask import Flask

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def print_hello():
    return 'hello there\n'

@celery.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return str(results) + '\n'

@celery.task
def return_text():
	with open("/home/ubuntu/data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3", 'r') as infile:
		rows = infile.readlines()

	filtered = list(filter(lambda x: x != '\n', rows))
	text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))

	return text

@app.route('/text', methods=['GET'])
def text():
	return return_text()

@app.route('/prime', methods=['GET'])
def prime():
	return gen_prime(100)

@app.route('/hello', methods=['GET'])
def hello():
	return print_hello()

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)