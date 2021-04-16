# Reproduction of Dragonnet

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

The first table is shown below. This table shows results for the IHDP dataset. It shows the mean absolute error (MAE) and standard error across simulations. The training and validation data are denoted with $\delta_{\text{in}}$, the test data (heldout data) is denoted with $\delta_{\text{out}}$ and these two combined is denoted with $\delta_{\text{all}}$.

| Method | $\delta_{\text{in}}$ | $\delta_{\text{out}}$ | $\delta_{\text{all}}$ |
|--------| ---------------------|------------------------|----------------------|
| baseline (TARNET) | 0.16 $\pm$ .01  | 0.21 $\pm$ .01  | 0.13 $\pm$ .00 |
| baseline + t-reg  | 0.15 $\pm$ .01  | 0.20 $\pm$ .01  | 0.12 $\pm$ .00 |
| Dragonnet         | 0.14 $\pm$ .01  | 0.21 $\pm$ .01  | 0.12 $\pm$ .00 |
| Dragonnet + t-reg | 0.14 $\pm$ .01  | 0.20 $\pm$ .01  | 0.11 $\pm$ .00 |

The second table is shown below. This table shows results for the ACIC 2018 dataset. Here, the error is the MAE of the average treatment effect estimate.

| Method | $\delta_{\text{all}}$ |
|--------| ----------------------|
| baseline (TARNET) | 1.45  |
| baseline + t-reg  | 1.40  |
| Dragonnet         | 0.55  |
| Dragonnet + t-reg | 0.35  |

### Reproduction

As the basis of our reproduction, we used the existing codebase for this paper. Since the codebase includes deprecated functions and old versions of python modules, we first upgraded the codebase to be compatible with newer module versions. This took some time as the method of finding old python code was to fix every single error we encountered when we ran the codebase. Eventually, we got the code working with the new versions of the modules. We upgraded the parts of the codebase necessary to run the experiments described in the original repository. The resulting codebase of this can be found on our [repository](https://github.com/skulane/ReprodcutionPaper). With our modification to the code base working and running as it should, we focussed on reproducing the tables that are shown above.

The first task was to produce tables using the smaller but already provided dataset of IHDP consisting of 50 replications. This gave us the following result.

```
{'tarnet': {'baseline': 0.16446090670469127, 'targeted_regularization': 0.15715158759816783}, 'dragonnet': {'baseline': 0.14885343353712469, 'targeted_regularization': 0.15495526943678933}, 'nednet': {'baseline': 0, 'targeted_regularization': 0}}
the tmle estimator result is this
{'tarnet': {'baseline': 0.14394802299946963, 'targeted_regularization': 0.1574912292756635}, 'dragonnet': {'baseline': 0.17765864595033992, 'targeted_regularization': 0.18212513156817756}, 'nednet': {'baseline': 0, 'targeted_regularization': 0}}
```
Translated to table it looks like this.
| Method | $\delta_{\text{all}}$ |
|--------| ----------------------|
| baseline (TARNET) | 0.164  |
| baseline + t-reg  | 0.157  |
| Dragonnet         |0.149 |
| Dragonnet + t-reg | 0.155  |

We run our experiments first locally and then on Google Cloud. We have made use of two types of VM instances. Both using ubunutu 20.04 lts as its operating system. Initially we ran our experiments on machine type e2-medium (2 vCPUs, 4 GB memory). Eventually we had switched to a more powerefull machine type c2-standard-4 (4 vCPUs, 16 GB memory).

### Lalonde dataset

In addition to reproduction the results from the paper, we wanted to see whether dragonnet can perform well on datasets in different domains. To do this, we use the [lalonde dataset](http://sekhon.berkeley.edu/matching/lalonde.html). This dataset was originally used to evaluate propensity score matching. It was collected for a study which investigated the effectiveness of a job training program done in 1974 on the real earnings of a person in 1978.

It contains 614 observations and 12 variables. From these variables we choose to use two continuous variables (`age` and `edu`) and four binary variables (`black`, `hisp`, `married` and `nodegr`) as covariates $X$, the binary variable (`treat`) as treatment $T$ and the continuous variable (`re78`) as outcome $Y$. We have created a summary of the variables we use in the table below. The statistics that are shown were created by Romain Guion in [this notebook](https://rugg2.github.io/Lalonde%20dataset%20-%20Causal%20Inference.html).

| Variable | Description | Mean | Standard deviation |
|----------|-------------|------|--------------------|
| `age`    | Age in years | 27.4 | 9.9 |
| `edu`    | Years of schooling | 10.3 | 2.6 |
| `black`  | Indicator variable for blacks | 0.4 | 0.5 |
| `hisp`   | Indicator variable for hispanics | 0.1 | 0.3 |
| `married`| Indicator variable for marital status | 0.4 | 0.5 |
| `nodegr` | Indicator variable for high school diploma | 0.6 | 0.5 |
| `re78`   | Real earnings in 1978 | 6792.8 | 7470.7 |
| `treat`  | An indicator variable for treatment status | 0.3 | 0.5 |

To create dragonnet for this dataset, we created the script [`run_lalonde.sh`](https://github.com/skulane/ReprodcutionPaper/blob/main/claudiashi57/dragonnet/src/experiment/run_lalonde.sh) in the original dragonnet repository. We also created the scripts [`lalonde_data.py`](https://github.com/skulane/ReprodcutionPaper/blob/main/claudiashi57/dragonnet/src/experiment/lalonde_data.py) to process the lalonde dataset and [`lalonde_main.py`](https://github.com/skulane/ReprodcutionPaper/blob/main/claudiashi57/dragonnet/src/experiment/lalonde_main.py) to create the models. After the models have been created, the results can be processed using the last script we created, [`lalonde_ate.py`](https://github.com/skulane/ReprodcutionPaper/blob/main/claudiashi57/dragonnet/src/process_result/lalonde_ate.py). These scripts are based off the scripts written for the IHDP data. However, as explained previously, we struggled understanding the IHDP data and how it is handled in the dragonnet repository. After much searching, we found out the purpose of the variables which in the code are referred to as `mu_0`, `mu_1` and `y_cf`. While `y_cf` records counterfactual outcomes and does not seem to be necessary to reproduce the results, we found out that `mu_0` and `mu_1` are the treated and control conditional means which are used to calculate the scores. Since the lalonde dataset is not a synthetic dataset, it does not contain these conditional means. Thus, the method of calculating the ATE score as for the IHDP data does not work for the lalonde dataset.

We decided to take a look at how the ATE score is calculated for the ACIC dataset. Here, no conditional means are used. Instead, only what is referred to as the 'ground truth' is used. From reading the code, we understand that this ground truth is supposed to be the effect size. For the ACIC dataset the effect size is recorded in some file called `params.csv`. There is nu such file for the lalonde dataset. Therefore, we resort to calculating the effect size ourselves. We assume that the effect size recorded for ACIC is the Cohen's d. This metric is the difference between two means divided by the standard deviation of the data. The two means are the means of on the one hand the data entries for which there was no treatment and on the other hand the data entries for which there was a treatment.

Now that we had written all of the code to create and evaluate dragonnet for the lalonde dataset, we were able to obtain our results. We found that the dragonnet with targeted regularization had an absolute error of 0.1996 for a test set of 33% of the data. Because the source code was unclear to us, we unfortunately were not able to use the 63/27/10 split used by the authors. Recall that this error is the same metric as the one used for the ACIC data, so it is the MAE of the average treatment effect estimate. To determine whether this result is good, we have to compare it to the results of other models. We found an [paper by Tobias Hatt and Stefan Feuerriegel](https://arxiv.org/pdf/2101.08490.pdf). In this paper, the authors compare their newly proposed model against many other methods. Keeping in mind that our train/test/validation split is slightly different from the one used in this paper, our model performs worse than each of these methods, but it's performance is close to some. At this point, we notice that they also use the lalonde dataset in combination with dragonnet to estimate ATE. Their performance is a lot better than our reproduced result. We think it is highly likely that our train/test/split and the way we combined the scripts for IHDP and ACIC is the reason for these varying results.
