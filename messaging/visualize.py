import plotly.plotly as py
import plotly.tools as tls

import matplotlib.pyplot as plt

values = {'hon': 1171, 'denne': 33, 'den': 6512, 'han': 3888, 'denna': 116, 'tweets': 14701, 'hen': 101, 'det': 2475}

values['hon'] = values['hon'] / values['tweets']
values['denne'] = values['denne'] / values['tweets']
values['den'] = values['den'] / values['tweets']
values['han'] = values['han'] / values['tweets']
values['denna'] = values['denna'] / values['tweets']
values['hen'] = values['hen'] / values['tweets']
values['det'] = values['det'] / values['tweets']

normalized = [values['hon'], values['denne'], values['den'], values['han'], values['denna'], values['hen'], values['det']]
x = range(len(normalized))
width = 1/1.5

plt.bar(x, normalized, width, color="blue")

fig = plt.gcf()
plotly_fig = tls.mpl_to_plotly(fig)
py.iplot(plotly_fig, filename='mpl-basic-bar')