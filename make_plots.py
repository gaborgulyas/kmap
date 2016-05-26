import pickle
import matplotlib.pyplot as plt
from kmap import plot_kmap

def build_fingerprint_dataset(records, attr_ixs):
	data = []
	dict = []
	for r in records:
		attrs = str([r[_] for _ in attr_ixs])
		try:
			ix = dict.index(attrs)
		except ValueError:
			ix = len(dict)
			dict.append(attrs)
		data.append(ix)
	return data

# Note -- data attributes indexes are for the following
#  0 - age
#  1 - workclass
#  2 - fnlwgt
#  3 - education
#  4 - education-num
#  5 - marital-status
#  6 - occupation
#  7 - relationship
#  8 - race
#  9 - sex
# 10 - capital-gain
# 11 - capital-loss
# 12 - hours-per-week
# 13 - native-country
# 14 - salary (>50K, <=50K)
records = pickle.load(open("adult.p", "r"))

# Dataset-1: age, sex, native-country
data1 = build_fingerprint_dataset(records, attr_ixs=[0, 9, 13])
plot_kmap(data=data1, data_label="Age, sex, native-country", filename="kmap_attrnum=3", plot_annotation=[[1, 3], [100, 1000]], annotation_params=dict(radius=.1, linestyle=dict(color='r', width=2, style=':')), colormap=plt.cm.viridis)

# Dataset-2: age, sex, native-country, race, relationship, workclass
data2 = build_fingerprint_dataset(records, attr_ixs=[0, 9, 13, 8, 7, 1])
plot_kmap(data=data2, data_label="+ race, relationship, workclass", filename="kmap_attrnum=6", plot_annotation=[[1, 3], [100, 1000]], colormap=plt.cm.viridis)

# Dataset-3: age, sex, native-country, race, relationship, workclass, education, occupation, capital-gain
data3 = build_fingerprint_dataset(records, attr_ixs=[0, 9, 13, 8, 7, 1, 3, 6, 10])
plot_kmap(data=data3, data_label="+ education, occupation, capital-gain", filename="kmap_attrnum=9", plot_annotation=[[1, 3], [100, 1000]], annotation_params=dict(radius=.25), colormap=plt.cm.viridis)
