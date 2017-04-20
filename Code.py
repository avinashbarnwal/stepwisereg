import statsmodels.formula.api as smf
import rpy2.robjects as robjects
import numpy as np
import pandas as pd
import functools
from rpy2.robjects import pandas2ri
import re



def reduce_concat(x, sep=""):
    return functools.reduce(lambda x, y: str(x) + sep + str(y), x)


def forward_selected(data,null,full,respose):
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
null_temp=re.split('~',null_formula)
null_predic_com=null_temp[1].split('+')
null_predic=null_predic_com[1:len(null_predic_com)]
full_temp=re.split('~',full_formula)
full_predic_com=full_temp[1].split('+')
full_predic=full_predic_com[1:len(full_predic_com)]


start     = set(null_predic)
remaining = set(full_predic)
selected = null_predic
response='T_Y'
current_score, best_new_score = 10000000, 10000000
flag=0
step=5
    while remaining and current_score >= best_new_score and step >0:
        flag=flag+1
        print("WAIT")
        print(flag)
        print(flag)
        print(flag)
        print(flag)
        print("WAIT")
        scores_with_candidates = []
        flag1=0
        for candidate in remaining:
            flag1=flag1+1
            print(flag1)
            formula = "{} ~ {} + 1".format(response,
                                           ' + '.join(selected + [candidate]))
            score = smf.ols(formula, data_complete5_py).fit().bic
            scores_with_candidates.append((score, candidate))
        scores_with_candidates.sort()
        best_new_score, best_candidate = scores_with_candidates.pop(0)
        if current_score > best_new_score:
            remaining.remove(best_candidate)
            print("BEST_NEW_SCORE")
            print(best_new_score)
            print("BEST_NEW_SCORE")
            print(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
        step=step-1    
    formula = "{} ~ {} + 1".format(response,
                                   ' + '.join(selected))
    model = smf.ols(formula, data).fit()
    return model


robjects.r['load']('data_complete5.RData')
data_complete5      = robjects.r['data_complete5']
data_complete5_py   = pandas2ri.ri2py(data_complete5)
Contains_E=pd.read_csv("Contains_E.csv",sep=",")
Contains_G=pd.read_csv("Contains_G.csv",sep=",")
Fourth_Select=pd.read_csv("Fourth_Select.csv",sep=",")
variable=Contains_E.append(Contains_G)
#variable.columns=['Variable']
Fourth_Select.columns=['Variable']
third_order=pd.DataFrame(['E7_cubrt','E5','E2_cubrt','G24','E7_1_x','E8_ex','G21','E8','G13','G27','G17','E2_E5','E5_E7','E2_E7','E2_E2','G10_G15_G24','G12_G13_G30','G12_G17_G27','G1_G17_G25'])
third_order.columns=['Variable']
variable_full=third_order.append(Fourth_Select)
full=reduce_concat(variable_full['Variable'],sep="+")
null=reduce_concat(third_order['Variable'],sep="+")
respose_add='T_Y~1+'
null_formula=respose_add+null
full_formula=respose_add+full




