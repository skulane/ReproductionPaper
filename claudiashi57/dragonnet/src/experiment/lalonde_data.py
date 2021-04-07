import pandas as pd
import numpy as np


def convert_file(x):
    x = x.values
    x = x.astype(float)
    return x


def load_and_format_covariates_ihdp(file_path='ReprodcutionPaper/data/lalonde/lalonde.csv'):

    # lalonde columns: treat","age","educ","black","hispan","married","nodegree","re74","re75","re78"
    data = np.loadtxt(file_path, delimiter=',')
    print('data loaded')

    x = data[:, 1:6]
    return x


def load_all_other_crap(file_path='ReprodcutionPaper/data/lalonde/lalonde.csv'):
    data = np.loadtxt(file_path, delimiter=',')
    t, y = data[:, 0], data[:, -1]
    return t.reshape(-1, 1), y.reshape(-1, 1)


def main():
    pass


if __name__ == '__main__':
    main()
