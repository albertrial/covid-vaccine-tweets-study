import numpy as np
import matplotlib.pyplot as plt
 
def barplot(x_ticks, y, title='', x_label='', y_label='', label_rotation=0):
	y_pos = np.arange(len(x_ticks))
	 
	# Create bars
	plt.bar(y_pos, y)
	 
	# Create names on the x-axis
	plt.xticks(y_pos, x_ticks, rotation=label_rotation)
	if label_rotation != 0:
		plt.subplots_adjust(bottom=0.4, top=0.99)
	 
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	# Show graphic
	plt.show()

