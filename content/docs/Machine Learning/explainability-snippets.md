version 2018

### Why Model interpretation?
Understanding how a model makes decisions — model interpretation — has been on the front burner since the end of 2017. Decision support systems and models they are based on don’t explain which features influenced their decisions were known as black boxes.
Model interpretability is not only important for companies that need to fulfill legal obligations to customers. It serves a technical purpose as well. Every ML model considers input features (problem properties) to predict results (outputs). The more relevant features we create and use to train an ML model during feature engineering, the more accurate results we can get and the simpler our model is. That’s why the ability to understand how the model makes predictions is crucial for its debugging.
[source](https://www.kdnuggets.com/2019/02/ai-data-science-advances-trends.html)

### What is model interpretability?
Machine learning models are very complex tools, so-called black-box classifiers, that don’t offer straightforward and human-interpretable decision rules.

As data scientists, we should be able to provide an explanation to end users about how a model works. However, this not necessarily means understanding every piece of the model or generating a set of decision rules.
There could also be a case where this is not required:
  * problem is well studied,
  * model results has no consequences,
  * understanding the model by the end-user could pose a risk of gaming the system.

[source](https://www.kdnuggets.com/2019/05/interpretability-machine-learning-models.html)

### How to do it?
  * Feature importance analysis
  * Feature correlations
  * Existing packages and tools (LIME, SHAP, Manifold...)
  
### Model Interpretation Guidelines
  * Global Interpretability: How well can we understand the relationship between each feature and the predicted value at a global level — for our entire observation set. Can we understand both the magnitude and direction of the impact of each feature on the predicted value?
  * Local Interpretability: How well can we understand the relationship between each feature and the predicted value at a local level — for a specific observation.
  * Feature Selection: Does the model help us focus on only the features that matter? Can it zero out the features that are just “noise”?

We can quickly identify that Feature X may be the most important, but does it make Outcome Y more or less likely? There may not be a yes-or-no answer.

### Resources
#### Blogs and Forums
- https://www.kdnuggets.com/2019/02/ai-data-science-advances-trends.html
- https://towardsdatascience.com/interpretability-in-machine-learning-70c30694a05f
- http://www.cse.chalmers.se/~richajo/dit866/lectures/l4/Feature%20ranking%20examples.html
- https://blog.dominodatalab.com/shap-lime-python-libraries-part-1-great-explainers-pros-cons/
- https://slundberg.github.io/shap/notebooks/Iris%20classification%20with%20scikit-learn.html
- https://slundberg.github.io/shap/notebooks/League%20of%20Legends%20Win%20Prediction%20with%20XGBoost.html
- https://forums.fast.ai/t/feature-importance-of-random-forest-vs-xgboost/17561/2
- https://github.com/parrt/random-forest-importances
- https://github.com/scikit-learn/scikit-learn/pull/13146
- https://towardsdatascience.com/be-careful-when-interpreting-your-features-importance-in-xgboost-6e16132588e7
- https://www.datascience.co.il/blog
- https://christophm.github.io/interpretable-ml-book/

#### Papers
- “Why Should I Trust You?” Explaining the Predictions of Any Classifier  https://arxiv.org/pdf/1602.04938.pdf
- LIME - an Introduction
https://www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime
- http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.pdf
- Interpretable machine learning: definitions, methods, and applications
https://arxiv.org/pdf/1901.04592.pdf
- https://web.stanford.edu/~hastie/Papers/ESLII.pdf

