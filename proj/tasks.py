from celery import shared_task

@shared_task
def hello():
    return 'Hello there!'

@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@shared_task
def return_text(data_path):
    with open(data_path, 'r') as infile:
        rows = infile.readlines()

    filtered = list(filter(lambda x: x != '\n', rows))
    text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))

    return str(text)


