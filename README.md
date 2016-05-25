# `kmap`: a script for visualizing anonymity set sizes in data

## What is this?

The idea originates from the question how to visualize what is happening with attributes in your data: how unique are the entities in your data. The only visualization that I am aware of is Fig. 3 in the [Panopticlick experiment](https://panopticlick.eff.org/static/browser-uniqueness.pdf), which shows anonymity set sizes created by each value of each attribute:

![alt text](https://raw.githubusercontent.com/gaborgulyas/kmap/master/images/panopticlick.png "Anonymity set sizes according to attributes in the Panopticlick experiment.")

While this is a nice figure, it is quite hard to understand it quantitatively, and it can be even more complicated if you want to compare different datasets by using this visualization method. However, it would be nice to understand the state of uniqueness in datasets, especially if you consider different attributes in each case, apply anonymization or other countermeasures to decrease uniqueness.

This is what `kmaps` was created for.

## Are there any instances where `kmaps` was used?

1. `Gabor Gyorgy Gulyas, Gergely Acs, Claude Castelluccia: Near-Optimal Fingerprinting with Constraints. PET Symposium 2016. (conditionally accepted paper)`
  Repository: [https://github.com/gaborgulyas/constrainted_fingerprinting](https://github.com/gaborgulyas/constrainted_fingerprinting)
