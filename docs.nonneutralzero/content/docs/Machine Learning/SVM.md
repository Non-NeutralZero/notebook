# SVM

*   P: ***We want to figure out a way to separate data into classes***
*   S: A linear classifier can help. Its objective would be to divide data using a hyperplane, and since the data points, from each class, that are closer to the classifier will be helping us decide on the orientation and position of the classifier, we can give them a fancy name (Support vectors) and call our linear classifier, the Support Vector Classifier. 
*   P: ***But, If the data is "clearly" separable, then we won't have one classifier - we would actually end up with so many possibilities to choosing one hyperplane AND we have to make sure future predictions are more likely to be correctly classified***
*   S: We could choose the one that insures the maximum distance between the Support vectors of the two classes (we'll call it a **maximum margin classifier**.) That way, we'll seperate the existing data, and have more confidence in classifying future data points.
*   P: ***We'll be looking to maximize the margin between the data points and the hyperplane, how do we do that?***
*   S: Hinge Loss!
*   P: ***Overfitting, this type of classifier would be very sensitive to outliers for example***
*   S: Explorative data analysis, outliers analysis or allow misclassification (more on that below). 