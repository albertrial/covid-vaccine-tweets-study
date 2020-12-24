import numpy as np
import matplotlib.pyplot as plt
 
def barplot(x_ticks, y, title='', x_label='', y_label=''):
	y_pos = np.arange(len(x_ticks))
	 
	# Create bars
	plt.bar(y_pos, y)
	 
	# Create names on the x-axis
	plt.xticks(y_pos, x_ticks)
	 
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	# Show graphic
	plt.show()
