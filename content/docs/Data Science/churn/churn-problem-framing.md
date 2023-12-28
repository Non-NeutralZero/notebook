# Churn - Problem Framing

## Churn reporting
1. What happened? (Inactive point of view)
   * In general cohorts work good here: start with a small population of churners and follow them over time
   * Clustering churners based on project and modeling bottom line
   * Example of small population of churners => “Churners who generate more profits, churns who explicitly expressed their insatisfaction”: or choose another prioritization criterion
   * Monetary retention rates (monetary churn)
   * Reversed cohorts: start with the churn date (Month / Year) and follow the churners retrospectively
   * Product / offers / segments cohorts
   * Maybe change of nomenclature/perspective to make problem framing more accessible to other shareholders (Product Churn, Account Churn, Usage Churn...etc)
 
2. Why did it happen?
   * Events that lead to customer churn (What are their existing pain points? Start with the possible obvious ones: bad customer service, non stop service, bad onboarding, no ongoing customer success plans, customers not using their accounts)
   * What factors are driving churn? What are customer attrition rates? Does customer tenure differ for group A vs. B?
   * Survival modeling (Cox, Nelson Aalen) -> Interpretable models, cohort comparison, time-specific predictions

3. Are there any returning customers?
   * Why are they returning? 
   * What are the recapture triggers?
   * What did they need to overcome their pain points?
   * What are the return dates? Is there a trend? A seasonality? CLT Events? 
   * Do they have multiple churn dates? (are there any customers who churned after their return)


## Churn inference
1. What kinds of models to test?
   * classification methods
   * survival regression methods
   * latent probability models
   * graph neural networks
2. How test these models for accuracy?
3. How often should the models be refreshed? What could be automated?
4. How long before new user behavior is reflected in predictions? Is there a distinction that should be taken into account from business stakeholders? Can some model or label drifts be anticipated ?
5. What is the process to incorporate new streams of data?
6. Are predictions actionable at the individual user level or only as a coarse segmentation?
7. How will predictions learn from implemented users retention actions?
8. What is the lift seen when using churn predictions?
9. How is that lift augmented after implemented users retention actions?
10. What is the Probability Threshold? How was is set?

## Churn monitoring
1. What is happening right now? (define indicators, metrics to monitor churn status)
2. What is the monitoring frequency that we should be employing?
3. Use descriptive models (not good for trend analysis, but good for summarizing what happened)
4. Compare/monitor different time periods (Beta distributions models are good enough)

## Adaptive churn analysis and prediction
1. Reactive churn management
2. Rigorous A/B testing 
3. Rentention analysis (What really generates retention, Retention based on Customer value - define customer value in context and problem scope)
4. Proactive churn management