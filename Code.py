import statsmodels.formula.api as smf
import rpy2.robjects as robjects
import numpy as np
import pandas as pd
import functools
from rpy2.robjects import pandas2ri
import re



def reduce_concat(x, sep=""):
    return functools.reduce(lambda x, y: str(x) + sep + str(y), x)


def forward_selected(data,null_formula,full_formula,respose,step):
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
    null_temp        =re.split('~',null_formula)
    null_predic_com  =null_temp[1].split('+')
    null_predic      =null_predic_com[1:len(null_predic_com)]
    full_temp        =re.split('~',full_formula)
    full_predic_com  =full_temp[1].split('+')
    full_predic      =full_predic_com[1:len(full_predic_com)]
    indices          = [i for i,id in enumerate(full_predic) if id not in null_predic]

    domain           =[full_predic[i] for i in indices]


    start            = set(null_predic)
    remaining        = set(domain)
    selected         = null_predic
    response         ='T_Y'
    current_score, best_new_score = 10000000, 10000000
    score_bic        =[]
    variable_added   =[]
    flag=0
    step=2
    while (remaining and current_score == best_new_score and step >0):
        scores_with_candidates = []
        for candidate in remaining:
            formula = "{} ~ {} + 1".format(response,
                                           ' + '.join(selected + [candidate]))
            score = smf.ols(formula, data_complete5_py).fit().bic
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
    formula = "{} ~ {} + 1".format(response,
                                   ' + '.join(selected))
    model = smf.ols(formula, data).fit()
    return model
    
    
    ##R like null and full models
    #null='y~1+var1'
    #full='y~1+var1+var2'
    
    
    
