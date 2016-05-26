# `kmap`: a script for visualizing anonymity set sizes in data

## What is this?

The idea originates from the question how to visualize what is happening with attributes in your data: how unique are the entities in your data. The only visualization that I am aware of is Fig. 3 in the [Panopticlick experiment](https://panopticlick.eff.org/static/browser-uniqueness.pdf), which shows anonymity set sizes created by each value of each attribute:

![alt text](https://raw.githubusercontent.com/gaborgulyas/kmap/master/images/panopticlick.png "Anonymity set sizes according to attributes in the Panopticlick experiment.")

While this is a nice figure, it is quite hard to understand it quantitatively, and it can be even more complicated if you want to compare different datasets by using this visualization method. However, it would be nice to understand the state of uniqueness in datasets, especially if you consider different attributes in each case, apply anonymization or other countermeasures to decrease uniqueness.

This is what `kmaps` was created for.

## Use-cases for `kmaps`

There are two use-cases of `kmaps` based on what we provide to it:

1. if we provide attribute classes of a complete dataset,
2. or if we provide anonymity sets that we have calculated.

In the first case, `kmaps` calculates anonymity sets. In the second case, it is assumed, that the provided anonymity sets are not partitioning the dataset. For example, lets consider that we create a [fingerprinta](https://github.com/gaborgulyas/constrainted_fingerprinting) for each users: a fingerprint is a set of attributes selected differently per user that identify them the most. However, there might be similar users, where most attributes are the same, thus fingerprinting will result in anonymity sets instead of characterizing a single user.

## Examples

In the examples below we use the [UCI Adult Data Set](https://archive.ics.uci.edu/ml/datasets/Adult) as a toy dataset.

### When attribute classes provided for the complete dataset 
The input for `kmaps` is a list of attributes, preferebly in an indexed fashion (to be faster). Like assume that we consider type of residences as

```python
attribute_dictionary = {("residence=urban", "age=0-21"): 0, ("residence=urban", "age=22-49"): 1, ("residence=urban", "age=50+"): 2, ("residence=rural", "age=0-21"): 3, ...}
```

so we would have a list characterizing our dataset as

```python
data = [1, 0, 0, 1, 2, 3, ...]
```

This list of attributes can be provided to `kmaps`, which will calculate anonymity sets and make the plot based on that.

This will result in something like this:

`k=3` | `k=6` | `k=9`
:-------------------------:|:-------------------------:|:-------------------------: 
![alt text](https://raw.githubusercontent.com/gaborgulyas/kmap/master/images/kmap_attrnum%3D3.png "k=3") | ![alt text](https://raw.githubusercontent.com/gaborgulyas/kmap/master/images/kmap_attrnum%3D6.png "k=6") | ![alt text](https://raw.githubusercontent.com/gaborgulyas/kmap/master/images/kmap_attrnum%3D9.png "k=9")

Here you can see that how anonymity sets change when we release the Adult Dataset with 3, 6 or 9 attributes.

### When anonymity sets are provided
We can also calculate a [fingerprinta](https://github.com/gaborgulyas/constrainted_fingerprinting) for each user, then check what is the user or anonymity set selected by each fingerprint. In this case we have to provide a dictionary where keys are anonymity set sizes, values are the frequency of such sets, like

```python
data = {1: 9994, 2: 6, ...}
```

After providing this input, `kmaps` will output something like this:

![alt text](https://raw.githubusercontent.com/gaborgulyas/kmap/master/images/individual_anonsetsizes.png "Anonymity set sizes by fingerprints")

## Parameters

Basically there is a single mandatory parameter and there are a lot of optional ones. By default this is how `kmaps` should be called:

```python
from kmap import plot_kmap

# First type of use: anonymity sets partition data
data = [1, 0, 0, 1, 2, 3, ...]
plot_kmap(data=data)

# Second type of use: anonymity sets created by something else, like fingerprints
data = {1: 9994, 2: 6, ...}
plot_kmap(data=[sum(data.values()), data])
```


## Are there any instances where `kmaps` was used?

Please [inform me](https://gulyas.info), if you use `kmaps`, or know further uses than listed here. Thanks.

1. `Gabor Gyorgy Gulyas, Gergely Acs, Claude Castelluccia: Near-Optimal Fingerprinting with Constraints. PET Symposium 2016.`

  Repository: [https://github.com/gaborgulyas/constrainted_fingerprinting](https://github.com/gaborgulyas/constrainted_fingerprinting)
