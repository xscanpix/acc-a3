from celery import shared_task

@shared_task
def hello():
    return 'Hello there!'

@shared_task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return str(results) + '\n'

@shared_task
def return_text(data_path):
	with open(data_path, 'r') as infile:
		rows = infile.readlines()

	filtered = list(filter(lambda x: x != '\n', rows))
	text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))

	return str(text)


