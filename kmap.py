##
# Copyright (c) 2016, Gabor Gyorgy Gulyas
# Email: gulyas@pet-portal.eu
# Web: gulyas.info
##

from collections import Counter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
from scipy.stats import gaussian_kde
from selectpoints import selectpoints # https://github.com/gaborgulyas/SelectPoints
import scipy.interpolate
import sys

def reverse_colourmap(cmap, name = 'my_cmap_r'):
	reverse = []
	k = []

	for key in cmap._segmentdata:
		k.append(key)
		channel = cmap._segmentdata[key]
		data = []

		for t in channel:
			data.append((1-t[0],t[2],t[1]))
		reverse.append(sorted(data))

	LinearL = dict(zip(k,reverse))
	my_cmap_r = matplotlib.colors.LinearSegmentedColormap(name, LinearL)
	return my_cmap_r

def add_annotations(ax, x, y, z, textsize, tail_threshold = None):
	min_xy = []
	min_s = 0.0
	max_xy = []
	max_s = 0.0
	if tail_threshold == None and len(x) > 8:
		tail_border = sorted(x, reverse=True)[5]
	else:
		tail_border = tail_threshold
	for ix in range(len(y)):
		if x[ix] <= 3:
			min_s += z[ix]
			min_xy.append((x[ix], y[ix]))
		if len(x) > 8 and x[ix] >= tail_border:
			max_s += z[ix]
			max_xy.append((x[ix], y[ix]))
	min_auq = "%.2f" % ((min_s / sum(z)) * 100)
	max_auq = "%.2f" % ((max_s / sum(z)) * 100)

	print sum(z)
	print min_xy, min_auq

	for x_, y_ in min_xy:
		# print x_, y_
		ax.annotate(min_auq+"%",
            xy=(math.log(x_, 10), math.log(y_, 10)), xycoords='data',
            xytext=(1.9, 4), textcoords='data',
            size=textsize, va="center", ha="right",
            arrowprops=dict(color="k", arrowstyle="-", alpha=.3),
            color="k"
        )
	# print max_xy
	if tail_threshold != None:
		tail_treshold_line_end_x =  tail_threshold
		ax.plot([math.log(tail_threshold, 10), math.log(tail_treshold_line_end_x, 10)], [-0.5, 2.5], "k--", label=None)
		plt.text(math.log(tail_treshold_line_end_x, 10)+.1, 2.4, max_auq+"%", size=13)
		ax.annotate("",
            xy=(math.log(tail_treshold_line_end_x, 10)+.1, 2.25), xycoords='data',
            xytext=(math.log(tail_treshold_line_end_x, 10)+.5, 2.25), textcoords='data',
            size=textsize, va="bottom", ha="right",
            arrowprops=dict(color="k", arrowstyle="<-"),
            color="k"
        )
	elif len(x) > 8:
		for x_, y_ in max_xy:
			# print x_, y_
			ax.annotate(max_auq+"%",
	            xy=(math.log(x_, 10), math.log(y_, 10)), xycoords='data',
	            xytext=(3, 1.5), textcoords='data',
	            size=textsize, va="center", ha="right",
	            arrowprops=dict(color="k", arrowstyle="-", alpha=.3),
	            color="k"
	        )

def plot_kmap(data, data_raw=True, as_partitions=None, data_label = "", filename = "", plot_annotation = True, annotation_params=None, title = None, title_loc = "center", titlelabelsize=26, axlabelsize=22, textsize=16, annotationsize=13, tail_threshold=None, plot_legend = True, plot_scatter=True, scatter_ms = None, scatter_c='k', scatter_a=.5, scatter_m=r'.', plot_heatmap=True, colormap=plt.cm.Greys, plot_contour=False, plot_contour_lbls=False):
	# Plot basic setup
	matplotlib.rcParams.update({'font.size': textsize})
	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot(1, 1, 1)
	if title != None:
		plt.title(title, loc=title_loc, fontdict={'fontsize': titlelabelsize})
	ax.set_xlabel("Anonymity Set Size ($k$)")
	ax.set_ylabel("Num. Anonymity Sets at Size of $k$")
	plt.tick_params(axis='both', which='major', labelsize=axlabelsize)

	# Process data
	if data_raw:
		# Assumed that anonymity sets partition the dataset
		data_length = len(data)
		xy = Counter(Counter(data).values())
		x = [x_ for x_ in sorted(xy.keys())]
		y = [xy[ass] for ass in sorted(xy.keys())]
		if as_partitions == None or as_partitions == True:
			z = [ass*xy[ass] for ass in sorted(xy.keys())]
			w = [float(ass*xy[ass])/data_length for ass in sorted(xy.keys())]
		else:
			z = [xy[ass] for ass in sorted(xy.keys())]
			w = [float(xy[ass])/data_length for ass in sorted(xy.keys())]
	else:
		# Not assumed that anonymity sets partition the dataset (e.g., they could be overlapping)
		data_length = data[0]
		xy = data[1]
		x = [x_ for x_ in sorted(xy.keys())]
		y = [xy[ass] for ass in sorted(xy.keys())]
		if as_partitions == None or as_partitions == False:
			z = [xy[ass] for ass in sorted(xy.keys())]
			w = [float(xy[ass])/data_length for ass in sorted(xy.keys())]
		else:
			z = [ass*xy[ass] for ass in sorted(xy.keys())]
			w = [float(ass*xy[ass])/data_length for ass in sorted(xy.keys())]

	if plot_heatmap or plot_contour:
		# Emphasize heavy spots for the contour (but visualize only one for each)
		x_ = []
		y_ = []
		z_ = []
		for ix in range(len(z)):
			for i in range((z[ix])):
				if i == 0:
					if scatter_ms == None:
						z_.append(float(10000*z[ix])/data_length)
					else:
						z_.append(scatter_ms)
				else:
					z_.append(0.0)

				x_.append(math.log(x[ix], 10))
				y_.append(math.log(y[ix], 10))

		# Heatmap calculation
		X, Y = np.mgrid[-0.5:5:100j, -0.5:5:100j]
		positions = np.vstack([X.ravel(), Y.ravel()])
		values = np.vstack([x_, y_])
		kernel = gaussian_kde(values)
		Z = np.reshape(kernel(positions).T, X.shape)
		Z = np.sqrt(np.sqrt(Z)) # Strengthen low-weighted regions

		# Plot heatmap
		if plot_heatmap:
			plt.contourf(X, Y, Z, 10, cmap=colormap, alpha=.5)

		# Plot contour
		if plot_contour:
			cs = plt.contour(X, Y, Z, 10, cmap=colormap, alpha=.5)
			if plot_contour_lbls:
				plt.clabel(cs, inline=1, fontsize=int(textsize/2))

	if plot_scatter:
		# Scatter points
		plt.scatter([math.log(_, 10) for _ in x], [math.log(_, 10) for _ in y], s=[10**4*_ for _ in w], alpha=scatter_a, c=scatter_c, marker=scatter_m, label = data_label) # alpha=.5,

		if plot_legend:
			# Legend
			lgnd = plt.legend(loc="upper right", fontsize=textsize) # , numpoints=1
			lgnd.legendHandles[0]._sizes = [30]


	# Select groups of datapoints
	if isinstance(plot_annotation, list):
		grps = [[] for _ in range(len(plot_annotation))]
		weights = [0.0 for _ in range(len(plot_annotation))]

		for ix in range(len(x)):
			for gix in range(len(plot_annotation)):
				grp = plot_annotation[gix]
				if x[ix] >= min(grp) and x[ix] <= max(grp):
					grps[gix].append([x[ix], y[ix]])
					weights[gix] += w[ix]

		for gix, grp in enumerate(grps):
			if len(grp) == 0:
				continue

			annotation_radius=.1
			if isinstance(annotation_params, dict) and 'radius' in annotation_params:
				if isinstance(annotation_params['radius'], list):
					annotation_radius = annotation_params['radius'][gix]
				else:
					annotation_radius = annotation_params['radius']
			annotation_distance=1.0
			if isinstance(annotation_params, dict) and 'distance' in annotation_params:
				if isinstance(annotation_params['radius'], list):
					annotation_distance = annotation_params['distance'][gix]
				else:
					annotation_distance = annotation_params['distance']
			annotation_linestyle=dict(color='r', width=2, style='-')
			if isinstance(annotation_params, dict) and 'linestyle' in annotation_params:
				annotation_linestyle = annotation_params['linestyle']

			pts = [[math.log(pt[0], 10), math.log(pt[1], 10)] for pt in grp]
			c, r = selectpoints(ax, pts, radius=annotation_radius, ec=annotation_linestyle['color'], lw=annotation_linestyle['width'], ls=annotation_linestyle['style'], fill=False)

			annotation_shift_vector = [r*annotation_distance, 0.0]
			if isinstance(annotation_params, dict) and 'location' in annotation_params:
				if isinstance(annotation_params['location'], list):
					if annotation_params['location'][gix] == 'left':
						annotation_shift_vector = [-r*annotation_distance, 0.0]
					elif annotation_params['location'][gix] == 'top':
						annotation_shift_vector = [0.0, r*annotation_distance]
					elif annotation_params['location'][gix] == 'bottom':
						annotation_shift_vector = [0.0, -r*annotation_distance]
				else:
					if annotation_params['location'] == 'left':
						annotation_shift_vector = [-r*annotation_distance, 0.0]
					elif annotation_params['location'] == 'top':
						annotation_shift_vector = [0.0, r*annotation_distance]
					elif annotation_params['location'] == 'bottom':
						annotation_shift_vector = [0.0, -r*annotation_distance]

			plt.text(c[0]+annotation_shift_vector[0], c[1]+annotation_shift_vector[1], "%.2f %%" % (weights[gix] * 100))

	# Add annotations for minimum and maximum anonymity sets
	elif isinstance(plot_annotation, bool) and plot_annotation:
		add_annotations(ax, x, y, z, annotationsize, tail_threshold)

	# Setup XY axes
	maxval = 5
	plt.ylim(-0.5, maxval)
	plt.xlim(-0.5, maxval)
	ticks = range(maxval+1)
	lbls = ["${10}^{%d}$" % v for v in range(maxval)]
	ax.set_xticks(ticks)
	ax.set_xticklabels(lbls)
	ax.set_yticks(ticks)
	ax.set_yticklabels(lbls)

	# Save file
	plt.tight_layout()
	if '.' in filename:
		plt.savefig(filename)
	else:
		plt.savefig(filename+'.pdf')
		plt.savefig(filename+'.png')