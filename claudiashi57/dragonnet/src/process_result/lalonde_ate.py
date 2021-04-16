#!/usr/bin/python

import copy
import sys
#sys.path.append("..")

import numpy as np
from numpy import load
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr

# from semi_parametric_estimation.ate import *
from ate import *

def cohend(d1, d2):
	# calculate the size of samples
	n1, n2 = len(d1), len(d2)
	# calculate the variance of the samples
	s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
	# calculate the pooled standard deviation
	s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
	# calculate the means of the samples
	u1, u2 = np.mean(d1), np.mean(d2)
	# calculate the effect size
	return (u1 - u2) / s


def load_truth(replication, knob):
    """
    loading ground truth data
    """

    file_path = '/Users/jessie/OneDrive/Documents/MSc/Q3/DL/ReprodcutionPaper/output/lalonde/{}/{}/simulation_outputs.npz'.format(knob, replication)
    data = load(file_path)
    treatment = data['t']
    outcome = data['y']

    outcome_0 = outcome[treatment == 0]
    outcome_1 = outcome[treatment == 1]

    effect_size = cohend(outcome_0, outcome_1)

    return effect_size


def load_data(knob='default', replication=1, model='baseline', train_test='test'):
    """
    loading train test experiment results
    """

    file_path = '/Users/jessie/OneDrive/Documents/MSc/Q3/DL/ReprodcutionPaper/output/lalonde/{}/'.format(knob)
    data = load(file_path + '{}/{}/0_replication_{}.npz'.format(replication, model, train_test))

    return data['q_t0'].reshape(-1, 1), data['q_t1'].reshape(-1, 1), data['g'].reshape(-1, 1), \
           data['t'].reshape(-1, 1), data['y'].reshape(-1, 1), data['index'].reshape(-1, 1), data['eps'].reshape(-1, 1)


def get_estimate(q_t0, q_t1, g, t, y_dragon, index, eps, truncate_level=0.01):
    """
    getting the back door adjustment & TMLE estimation
    """

    psi_n = psi_naive(q_t0, q_t1, g, t, y_dragon, truncate_level=truncate_level)
    psi_tmle, psi_tmle_std, eps_hat, initial_loss, final_loss, g_loss = psi_tmle_cont_outcome(q_t0, q_t1, g, t,
                                                                                              y_dragon,
                                                                                              truncate_level=truncate_level)
    return psi_n, psi_tmle, initial_loss, final_loss, g_loss


def make_table(train_test='train', n_replication=1):
    dict = {'tarnet': {'baseline': {'back_door': 0, }, 'targeted_regularization': 0},
            'dragonnet': {'baseline': 0, 'targeted_regularization': 0},
            'nednet': {'baseline': 0, 'targeted_regularization': 0}}
    tmle_dict = copy.deepcopy(dict)
    rmsd_dict = copy.deepcopy(dict)

    for knob in ['dragonnet', 'tarnet']:
        for model in ['baseline', 'targeted_regularization']:

            errors, tmle_errors, rmsd_errors = [], [], []
            for rep in range(n_replication):
                q_t0, q_t1, g, t, y_dragon, index, eps = load_data(knob, rep, model, train_test)
                psi_n, psi_tmle, initial_loss, final_loss, g_loss = get_estimate(q_t0, q_t1, g, t, y_dragon, index, eps, truncate_level=0.01)

                truth = load_truth(rep, knob)
                err = abs(psi_n - truth)
                tmle_err = abs(psi_tmle - truth)
                rmsd_err = (psi_n - truth)**2

                errors.append(err)
                tmle_errors.append(tmle_err)
                rmsd_errors.append(rmsd_err)

        dict[knob][model] = np.mean(errors)
        tmle_dict[knob][model] = np.mean(tmle_errors)
        rmsd_dict[knob][model] = np.sqrt(np.mean(rmsd_errors))

    return dict, tmle_dict, rmsd_dict


def main():
    dict, tmle_dict, rmsd_dict = make_table()
    print("The back door adjustment result is below")
    print(dict)

    print("the rmsd estimator result is this ")
    print(rmsd_dict)


if __name__ == "__main__":
    main()
