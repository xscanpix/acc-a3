import json

def main():
	with open("/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6", "r") as infile:
		rows = infile.readlines()
                
	filtered = list(filter(lambda x: x != '\n', rows))
	text = list(map(lambda x: json.loads(x)['text'].encode('utf-8'), filtered))
    text_no_rt = list(filter(lambda x: x[:2] != 'RT', text))

    pronouns = 
 	{
	    'han': 0,
	    'hon': 0,
	    'hen': 0,
	    'det': 0,
	    'denna': 0,
	    'denne': 0,
	    'den': 0
    }

    for row in text_no_rt:
    	pronouns = count_words(pronouns, row)
    

    pronouns_json = json.dumps(pronouns)
    print pronouns_json
        
def count_words(dic, text):
        words = str.split(text)
        for word in words:
                if word in dic:
                        dic[word] += 1
        return dic

if __name__ == '__main__':
	main()