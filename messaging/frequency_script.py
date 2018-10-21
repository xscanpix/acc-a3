def main():
	with open("/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6", "r") as infile:
		rows = infile.readlines()

	filtered = list(filter(lambda x: x != '\n', rows))
	text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))

	print text[0]



if __name__ == '__main__':
	main()