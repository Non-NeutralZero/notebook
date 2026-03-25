# source https://scikit-learn.org/stable/modules/tree.html#classification
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn import tree
import pandas as pd

iris = load_iris()
X, y = load_iris(return_X_y=True)
X_df = pd.DataFrame(X, columns=iris.feature_names)
X_df.head()

# Imagine we need to pick a root node ourselves: we'll need to see how each feature performs on the split
## Fitting our tree on the train data
import matplotlib.pyplot as plt

for feature in iris.feature_names:
  plt.figure(figsize=(10,6))
  clf = tree.DecisionTreeClassifier(max_depth=1)
  clf = clf.fit(X_df.loc[:,feature].values.reshape(-1,1), y)
  print("Decision tree based on {0}".format(feature))
  tree.plot_tree(clf, filled=False, impurity=False) 
  plt.show()

# This process is already implemented in the sklearn library. 
## So let's look at what it yields!
clf = tree.DecisionTreeClassifier()
plt.figure(figsize=(20,10))
tree.plot_tree(clf.fit(X, y), impurity=True, feature_names=iris.feature_names) 
plt.show()

## Plotting the tree (alternative - useful when tree is big!)
import graphviz 
dot_data = tree.export_graphviz(clf, out_file=None) 
graph = graphviz.Source(dot_data) 
graph.render("iris")

dot_data = tree.export_graphviz(clf, out_file=None, 
                     feature_names=iris.feature_names,  
                     class_names=iris.target_names,  
                     filled=True, rounded=True,  
                     special_characters=True)  
graph = graphviz.Source(dot_data)  
graph 

# see also: plot Decision surface of a decision tree using paired features
# https://scikit-learn.org/stable/auto_examples/tree/plot_iris_dtc.html
