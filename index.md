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
This dataset was partially given in the existing repository linked to this paper.  This dataset is a synthetic dataset based on the Health and Development program. Which can be generated using the [NPCI R package availabe on github](https://github.com/vdorie/npci). In the paper 1000 replications are used.

### ACIC
This data set was part of a competition. The dataset is based on realworld records and is therefore also anonymized. Accec to this data can gotten only after agreeing to several condition, such as respecting the anonymization in the dataset. Both the ACIC dataset and the detailed description of the dataset can be found on the [ACIC 2018 Causal Inference Challenge](https://www.synapse.org/#!Synapse:syn11294478/wiki/).

## Experiments

We aim to replicate the results for both of thes above described datasets. This entails replicating two tables.

The first table is shown below. This table shows results for the IHDP dataset. It shows the mean absolute error and standard error across simulations. The training and validation data are denoted with $\delta_{\text{in}}$, the test data (heldout data) is denoted with $\delta_{\text{out}}$ and these two combined is denoted with $\delta_{\text{all}}$.

| Method | $\delta_{\text{in}}$ | $\delta_{\text{out}}$ | $\delta_{\text{all}}$ |
|--------| ---------------------|------------------------|----------------------|
| baseline (TARNET) | 0.16 $\pm$ .01  | 0.21 $\pm$ .01  | 0.13 $\pm$ .00 |
| baseline + t-reg  | 0.15 $\pm$ .01  | 0.20 $\pm$ .01  | 0.12 $\pm$ .00 |
| Dragonnet         | 0.14 $\pm$ .01  | 0.21 $\pm$ .01  | 0.12 $\pm$ .00 |
| Dragonnet + t-reg | 0.14 $\pm$ .01  | 0.20 $\pm$ .01  | 0.11 $\pm$ .00 |

The second table is shown below. This table shows results for the ACIC 2018 dataset.

| Method | $\delta_{\text{all}}$ |
|--------| ----------------------|
| baseline (TARNET) | 1.45  |
| baseline + t-reg  | 1.40  |
| Dragonnet         | 0.55  |
| Dragonnet + t-reg | 0.35  |

### Reproduction

We run our experiments on Google Cloud.

### Lalonde dataset

In addition to reproduction the results from the paper, we wanted to see whether dragonnet can perform well on datasets in different domains. To do this, we use the [lalonde dataset](http://sekhon.berkeley.edu/matching/lalonde.html). This dataset was originally used to evaluate propensity score matching. It contains 445 observations and 12 variables. These variables are the following:

| Variable | Description |
|----------|-------------|
| `age`    | Age in years |
| `edu`    | Years of schooling
| `black`  | Indicator variable for blacks |
| `hisp`   | Indicator variable for hispanics |
| `married`| Indicator variable for marital status |
| `nodegr` | Indicator variable for high school diploma |
| `re74`   | Real earnings in 1974 |
| `re75`   | Real earnings in 1975 |
| `re78`   | Real earnings in 1978 |
| `u74`    | Indicator variable for earnings in 1974 being zero |
| `u75`    | Indicator variable for earnings in 1975 being zero |
| `treat`  | An indicator variable for treatment status |
