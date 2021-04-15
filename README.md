# Reproduction of Dragonnet

Original repository :  https://github.com/claudiashi57/dragonnet \
Original Paper  : https://arxiv.org/pdf/1906.02120.pdf

In this project, we aim to reproduce results shown in the paper ['Adapting Neural Networks for the Estimation of Treatment effects' by Shi et al](https://arxiv.org/pdf/1906.02120.pdf). In this paper, the authors infer treatment outcomes from observational data. To do this, they use a neural network called [dragonnet](https://github.com/claudiashi57/dragonnet).

## Dragonnet

Dragonnet aims to perform causal inference using neural networks. **Causal inference** involves answering causal questions. An example of a causal question is "*Will I pass the course, given that I hand in this blog?*". This is a question about **prediction**. We can also ask questions about **intervention**: "*If I hand in this blog, will I pass the course?*". In these questions, the **dependent** variable is the passing of the course and the **independent** variable is the handing in of the blog. With these kinds of questions, we have to be careful about confounding data. **Confounding** data is data that influences our dependent and independent variable. In observational data, we have to be aware that we may be dealing with such confounding data.

The neural network is aimed at predicting **treatment effects**. We ask the question "*What is the expected effect of intervening by assigning a treatment?*". We refer to the **treatment** as $T$, the **outcome** as $Y$ and **covariates** as $X$. These covariates may influence both the treatment as well as the outcome. The **expected outcome** can be defined as follows:

$$Q(t, x) = \mathbb{E}[Y | t,x]$$

The authors also use a propensity score. A **propensity score** denotes the probability that someone is assigned a certain treatment given the covariates. These propensity scores may then be used to reduce bias by performing propensity score weighting. The formula for propensity score is the following:

$$g(x) = P(T = 1 | x)$$

Lastly, the authors of the paper describe the **Average Treatment Effect** (ATE) with the following formula:

$$\psi = \mathbb{E}[\mathbb{E}[Y | T=1, X] - \mathbb{E}[Y | T=0, X]]$$

The dragonnet network aims to model $Q$ as well as $g$. This is done by using a **three-headed architecture**. To make sure that the estimation of $\psi$ is good enough, they use **targeted regularization**. This is a regularization procedure that is based on non-parametric estimation theory.

The authors use a theorem by Rosenbaum and Rubin (1983) and determine that "if the average treatment effect $\psi$ is identifiable from observational data by adjusting for $X$, then adjusting for the propensity score also suffices". This can be written as follows:

$$\text{If } \mathbb{E}[\mathbb{E}[Y | T=1, X] - \mathbb{E}[Y | T=0, X]]\text{, then } \spi \mathbb{E}[\mathbb{E}[Y | T=1, g(X)] = \mathbb{E}[Y | T=0, g(X)]]$$

Based upon this theory, the authors create the architecture of dragonnet. Here, they estimate $\hat{Q}(t,x)$:

![](assets/README-6be6d88c.png)

## Datasets

Dragonnet is evaluated using two datasets: the Infant Health and Development program (IHDP) dataset from 2011 and the Atlantic Causal Inference Conference (ACIC) competition data from 2018.

### IHDP

### ACIC

## Experiments

### Reproduction

We run our experiments on Google Cloud.

### Lalonde
