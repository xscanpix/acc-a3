from celery import Celery
from flask import Flask
import json
import time

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
def return_text(data_path):
	with open(data_path, 'r') as infile:
		rows = infile.readlines()

	filtered = list(filter(lambda x: x != '\n', rows))
	text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))

	return str(text)

@app.route('/text', methods=['GET'])
def text():

	num_workers = 5

	data_paths = ["/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6",
				  "/home/ubuntu/data/094b1612-1832-429e-98c1-ae06e56d88d6", 
				  "/home/ubuntu/data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3",
				  "/home/ubuntu/data/0d7c752e-d2a6-474b-aef4-afe5dc506e33",
				  "/home/ubuntu/data/0ecdf8e0-bc1a-4fb3-a015-9b8dc563a92f"]

	result = return_text.delay(data_paths[0])

	print "Task finished? ", result.ready()
	print "Task result ", result.result

	time.sleep(10)

	print "Task finished? " + result.ready()
	print "Task result ", result.result


	return result.result

@app.route('/prime', methods=['GET'])
def prime():
	return gen_prime(100)

@app.route('/hello', methods=['GET'])
def hello():
	return print_hello()

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)