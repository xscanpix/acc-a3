from celery import Celery, group
from flask import Flask
import json
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

@celery.task(trail=True)
def return_text(data_path):
  with open(data_path, 'r') as infile:
    rows = infile.readlines()

  filtered = list(filter(lambda x: x != '\n', rows))
  text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))
  text_no_rt = list(filter(lambda x: x[:2] != 'RT', text))

  data = {'tweets': 0, 'han': 0,'hon': 0,'hen': 0,'det': 0,'denna': 0,'denne': 0,'den': 0}

  for row in text_no_rt:
    data = count_words(data, row)

 	data['tweets'] = len(text_no_rt)

  data_json = json.dumps(data)
        
  return data_json

def count_words(pronouns, text):
  words = str.split(text)
  for word in words:
    if word in pronouns:
      pronouns[word] += 1
  return pronouns

@celery.task(bind=True)
def task(self):
  data_paths = ["/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6",
                "/home/ubuntu/data/094b1612-1832-429e-98c1-ae06e56d88d6",
                "/home/ubuntu/data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3",
                "/home/ubuntu/data/0d7c752e-d2a6-474b-aef4-afe5dc506e33",
                "/home/ubuntu/data/0ecdf8e0-bc1a-4fb3-a015-9b8dc563a92f"]
  
  result = []
  for path in data_paths:
    result.append(return_text(path))

  return result

@celery.task(bind=True)
def task_parallel(self):
  data_paths = ["/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6",
                "/home/ubuntu/data/094b1612-1832-429e-98c1-ae06e56d88d6",
                "/home/ubuntu/data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3",
                "/home/ubuntu/data/0d7c752e-d2a6-474b-aef4-afe5dc506e33",
                "/home/ubuntu/data/0ecdf8e0-bc1a-4fb3-a015-9b8dc563a92f"]
  
  return group(return_text.s(path) for path in data_paths)()

@app.route('/longtask', methods=['GET'])
def longtask():
  res = task.apply_async()

  while(res.ready() == False):
  	time.sleep(1)

  result = res.result

  counts = {'tweets': 0, 'han': 0, 'hon': 0, 'hen': 0, 'det': 0, 'den': 0, 'denne': 0, 'denna': 0}
  for r in result:
    val = json.loads(r)

    counts['tweets'] += val['tweets']
    counts['han'] += val['han']
    counts['hon'] += val['hon']
    counts['hen'] += val['hen']
    counts['den'] += val['den']
    counts['det'] += val['det']
    counts['denne'] += val['denne']
    counts['denna'] += val['denna']

  return str(counts)

@app.route('/longtask_parallel', methods=['GET'])
def longtask_parallel():
  res = task_parallel()

  while(res.ready() == False):
  	time.sleep(1)

  counts = {'tweets': 0, 'han': 0, 'hon': 0, 'hen': 0, 'det': 0, 'den': 0, 'denne': 0, 'denna': 0}
  for r in res.results:
    val = json.loads(r.result)

    counts['tweets'] += val['tweets']
    counts['han'] += val['han']
    counts['hon'] += val['hon']
    counts['hen'] += val['hen']
    counts['den'] += val['den']
    counts['det'] += val['det']
    counts['denne'] += val['denne']
    counts['denna'] += val['denna']

  return str(counts)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)