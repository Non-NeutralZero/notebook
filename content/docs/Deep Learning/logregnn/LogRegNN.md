# Logistic Regression as a Neural Network

## Architecture

𝐺𝑖𝑣𝑒𝑛 𝑥 , 𝑦̂ = 𝑃(𝑦 = 1|𝑥), where 0 ≤ 𝑦̂ ≤ 1


Parameters of logistic regression
1.   Input observation,features matrix X
2.   Target vector Y
3.   Weights w
4.   Threshold or bias b
5.   Output: 𝑦̂, sigmoid(z) where z = 𝑤 𝑇 *𝑥 + 𝑏

To get the parameters w and b (i.e. learning), we optimize on:

𝐽(𝑤, 𝑏) = 1/m (∑ 𝐿(𝑦̂ (𝑖) , 𝑦 (𝑖) ))

i.e. 

𝐽(𝑤, 𝑏) = 1/m(∑ ylog((𝑦̂) + (1-y)(1-log(1-𝑦̂))))

## Implementation

[github/Non-NeutralZero - CatVsNonCat.ipynb](https://github.com/Non-NeutralZero/docs/blob/main/content/docs/Deep%20Learning/logregnn/CatVsNonCat.ipynb)

> [!NOTE]
> **Experimentation(s) output**
> [View notebook output](/notebook/outputs/CatVsNonCat-outputs/CatVsNonCat.html)
