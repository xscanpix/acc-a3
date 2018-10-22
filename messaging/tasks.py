from celery import Celery, group, shared_task
from flask import Flask
import json
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@shared_task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

@shared_task(bind=True)
def count_all_words():
  data_paths = ["/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6",
                "/home/ubuntu/data/094b1612-1832-429e-98c1-ae06e56d88d6",
                "/home/ubuntu/data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3",
                "/home/ubuntu/data/0d7c752e-d2a6-474b-aef4-afe5dc506e33",
                "/home/ubuntu/data/0ecdf8e0-bc1a-4fb3-a015-9b8dc563a92f"]

  result = group(return_text.s(t) for t in data_paths).delay()

  while(result.ready() == False):
    time.sleep(5)

  completed = {'han': 0,'hon': 0,'hen': 0,'det': 0,'denna': 0,'denne': 0,'den': 0}

  for res in result:
    completed['han'] += res.result['han']
    completed['hon'] += res.result['hon']
    completed['det'] += res.result['det']
    completed['denna'] += res.result['denna']
    completed['denne'] += res.result['denne']
    completed['den'] += res.result['den']
    completed['hen'] += res.result['hen']

  return completed

@shared_task()
def return_text(data_path):
  with open(data_path, 'r') as infile:
    rows = infile.readlines()

  filtered = list(filter(lambda x: x != '\n', rows))
  text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))
  text_no_rt = list(filter(lambda x: x[:2] != 'RT', text))

  pronouns = {'han': 0,'hon': 0,'hen': 0,'det': 0,'denna': 0,'denne': 0,'den': 0}

  for row in text_no_rt:
    pronouns = count_words(pronouns, row)

  pronouns_json = json.dumps(pronouns)
        
  return pronouns_json

def count_words(pronouns, text):
  words = str.split(text)
  for word in words:
    if word in pronouns:
      pronouns[word] += 1
  return pronouns

@app.route('/count', methods=['GET'])
def count():
  result = count_all_words()

  return result.result

  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)