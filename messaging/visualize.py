import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

values = {'hon': 1171, 'denne': 33, 'den': 6512, 'han': 3888, 'denna': 116, 'tweets': 14701, 'hen': 101, 'det': 2475}

values['hon'] = float(values['hon']) / float(values['tweets'])
values['denne'] = float(values['denne']) / float(values['tweets'])
values['den'] = float(values['den']) / float(values['tweets'])
values['han'] = float(values['han']) / float(values['tweets'])
values['denna'] = float(values['denna']) / float(values['tweets'])
values['hen'] = float(values['hen']) / float(values['tweets'])
values['det'] = float(values['det']) / float(values['tweets'])

print(values)

normalized = [values['hon'], values['denne'], values['den'], values['han'], values['denna'], values['hen'], values['det']]
objects = ["hon","denne","den","han","denna","hen","det"]
y_pos = np.arange(len(objects))
x = range(len(normalized))


plt.bar(y_pos, normalized, align='center')
plt.xticks(y_pos, objects)
plt.ylabel('Counts')
plt.title('Pronoun counts')
 
plt.show()