---
bookToc: true
---

## Types of outliers
### With regards to the distribution
- Univariate: can be found when looking at a distribution of values in a single feature space.
- Multivariate: can be found in a n-dimensional space (of n-features).
### With regards to the environment
- Point outliers: single data points that lay far from the rest of the distribution.
- Contextual outliers: can be noise in data, such as punctuation symbols when realizing
text analysis or background noise signal when doing speech recognition.
- Collective outliers: Collective outliers can be subsets of novelties in data such as a signal
that may indicate the discovery of new phenomena.

## Most common causes of outliers on a data set
- Data entry errors (human errors)
- Measurement errors (instrument errors)
- Experimental errors (data extraction or experiment planning/executing errors)
- Intentional (dummy outliers made to test detection methods)
- Data processing errors (data manipulation or data set unintended mutations)
- Sampling errors (extracting or mixing data from wrong or various sources)
- Natural (not an error, novelties in data)

{{< hint info >}} 
**Hint**

Outliers that are not a product of an error are called novelties. 
{{< /hint >}}

## Before starting the detection of outliers
- Which and how many features am I taking into account to detect outliers ? (univariate /
multivariate)
- Can I assume a distribution(s) of values for my selected features? (parametric /
non-parametric)

## Most popular methods for outlier detection
- Z-Score or Extreme Value Analysis (parametric): a metric that indicates how many
standard deviations a data point is from the sample’s mean, assuming a gaussian
distribution.
- Dbscan (Density Based Spatial Clustering of Applications with Noise): applied to detect
outliers in nonparametric distributions in many dimensions. it is focused on finding
neighbors by density (MinPts) on an ‘n-dimensional sphere’ with radius ɛ. A cluster can be
defined as the maximal set of ‘density connected points’ in the feature space.
- Isolation forests: isolation forests are an effective method for detecting outliers or
novelties in data. Isolation forest’s basic principle is that outliers are few and far from the
rest of the observations.
- Probabilistic and Statistical Modeling (parametric)
- Linear Regression Models (PCA, LMS)
- Proximity Based Models (non-parametric)
- Information Theory Models
- High Dimensional Outlier Detection Methods (high dimensional sparse data)

## Anomaly detection Literature
- Statistical AD techniques: fit a statistical model for normal behavior
- Density-based - ex: Local Outlier Factor (LOF) and variantes (COF ODINLOCI)
- Support estimation - OneClassSVM
- High-dimensional techniques: - Spectral Techniques - Random Forest - Isolation Forest