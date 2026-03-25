# Random Forest
Random forests are built from decision trees
1. Initially, the original data is bootstrapped by randomly sampling the data and creating a new dataset with the same size as the original one (to be able to do that, duplicated obs are allowed - aka random sampling with replacement)
1. Build a decision tree based on the bootsrapped data
1. Randomly select features (typically sqrt(n_features)) from the bootsrapped data when splitting nodes (this is called random subspace method)
1. Go back to step 1 and repeat

<!--more-->
*   ***does all the original data end up in the sampled subsets?*** For each created Decision Tree, the non-bootsrapped data is called **Out-of-Bag** data. 
*   ***once we get the forest, how do we use it?*** if we want to get a prediction, we run an obs through all the trees of the forest and pick the prediction with the most votes. (this process is called **Bagging**, i.e. **B**ootsrapping + **agg**regating single predictions)
*   ***how do we evaluate the random forest?*** we can evaluate it using the out-of-bag error, i.e. measure how accurate the forest predicts out-of-bag data. 
*   ***is there an optimal number of features for each bootsrapped sample?*** Yes. Given that we can measure the out-of-bag error, we can use it to compare forests built on different samples of features and select the one with the smallest error.
*   ***how many times should we repeat this processes?*** plot OOB error rate vs. number of trees 
*   ***Why are they called random forests?*** Because of the random sampling concept at step 1 and at step 3 
*   ***how is a forest better than one decision tree?*** By getting a large number of different (high variance ) trees 


For more, see Chapter 15 in https://web.stanford.edu/~hastie/Papers/ESLII.pdf