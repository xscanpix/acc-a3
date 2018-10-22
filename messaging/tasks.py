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
def count_words_all_files(self):

  data_paths = []
  for filename in os.listdir("home/ubuntu/data"):
    data_paths.append(os.path.join(directory, filename))
  
  return group(return_text.s(path) for path in data_paths)()

@app.route('/longtask', methods=['GET'])
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