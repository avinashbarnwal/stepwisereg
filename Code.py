# coding: utf-8

# In[8]:

import numpy as np
import sklearn
import warnings
import os
warnings.filterwarnings('ignore')
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import make_regression
from patsy import dmatrices
import statsmodels.formula.api as smf
import pandas as pd
import functools
import re


path = '/data_path'
os.chdir(path)

data = pd.read_csv("test_data.csv")
###########Train Dataset and Test Dataset Creation########
msk = np.random.rand(len(data_LUAD)) < 0.8
train = data[msk]
test = data[~msk]

#########Independent Variables are from 2:102 and 106 has Dependent Variable########
X_train = data.iloc[:,2:102]
Y_train = 10*data.iloc[:,106]

###########Changes in the name of columns######
columns         = list(X_train.columns.values)
columns_changes = map(lambda x:x.replace("-", "_"),columns)
X_train.columns = columns_changes
train = pd.concat([X_train,Y_train],axis=1)

X_test = test.iloc[:,2:102]
Y_test = 10*test.iloc[:,106]

columns_test         = list(X_test.columns.values)
columns_changes_test = map(lambda x:x.replace("-", "_"),columns_test)
X_test.columns = columns_changes_test
test = pd.concat([X_test,Y_test],axis=1)

##Creating the features concatenation
features = "+".join(columns_changes)

##Creating Null and Full formula
var1 = columns_changes[0]  
null = 'OS_MONTHS ~' + var1
full = 'OS_MONTHS ~' + features


# In[10]:

def reduce_concat(x, sep=""):
    return functools.reduce(lambda x, y: str(x) + sep + str(y), x)

def forward_selected(data,null_formula,full_formula,response,step,intercept):
    """Linear model designed by forward selection.
    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response
    response: string, name of response column in data
    Returns:
    --------
    model: an "optimal" fitted statsmodels linear model
           with an intercept
           selected by forward selection
           evaluated by bic
    """
    print(null_formula)
    print(full_formula)
    print(response)
    
    null_temp        = re.split('~',null_formula)
    null_predic_com  = null_temp[1].split('+')
    null_predic      = null_predic_com[1:len(null_predic_com)]
    full_temp        = re.split('~',full_formula)
    full_predic_com  = full_temp[1].split('+')
    full_predic      = full_predic_com[1:len(full_predic_com)]
    indices          = [i for i,id in enumerate(full_predic) if id not in null_predic]
    domain           = [full_predic[i] for i in indices]

    start            = set(null_predic)
    remaining        = set(domain)
    selected         = null_predic
    current_score, best_new_score = 10000000, 10000000
    score_bic        = []
    variable_added   = []
    flag=0
    step=2
    while (remaining and current_score == best_new_score and step >0):
        scores_with_candidates = []
        for candidate in remaining:
            formula = "{} ~ {}".format(response,' + '.join(selected + [candidate]))
            if intercept ==1:
                formula = formula + "-1"
            score = smf.ols(formula, data).fit().aic
            scores_with_candidates.append((score, candidate))
        scores_with_candidates.sort()
        best_new_score, best_candidate = scores_with_candidates.pop(0)
        if current_score > best_new_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            score_bic.append(best_new_score)
            variable_added.append(best_candidate)
            current_score = best_new_score
        step=step-1
    formula = "{} ~ {}".format(response,' + '.join(selected))
    if intercept ==1:
        formula = formula + "-1"
    model = smf.ols(formula, data).fit()
    return model

model           = forward_selected(train,null,full,'OS_MONTHS',50,0)

model_param     = model.params
print(model.summary())

test_predict = model.predict(test)
