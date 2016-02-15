import pickle
import os
import urllib2

# Obtaining data
if not os.path.exists("adult.data"):
	print "obtaining dataset...",
	response = urllib2.urlopen('http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data')
	f = open("adult.data", "w+")
	f.write(response.read())
	f.close()
	print "done!"

# Dataset init
attrib_dict = {}
for ix in range(15):
	attrib_dict[ix] = []
records = []

# Caching
print "caching data...",
for l in open("adult.data", "r").readlines():
	r_ = l.replace('\r', '').replace('\n', '').replace(', ', ',').split(',')

	if len(r_) < 15:
		continue

	r = []
	for ix, a in enumerate(r_):
		try:
			a_ix = attrib_dict[ix].index(a)
		except ValueError:
			a_ix = len(attrib_dict[ix])
			attrib_dict[ix].append(a)
		r.append(a_ix)
	records.append(r)
print "done!"

print "num records:", len(records)

# Writing to disk
print "writing cahce...",
pickle.dump(records, open("adult.p", "w+"))
pickle.dump(attrib_dict, open("attrib_dict.p", "w+"))
print "done!"