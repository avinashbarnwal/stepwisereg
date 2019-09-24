import pandas as pd
from stepwisereg import *

data = pd.read_csv("lung_cancer.csv")
###########Train Dataset and Test Dataset Creation########

msk = np.random.rand(len(data)) < 0.8
train = data[msk]
test  = data[~msk]

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
X_test.columns       = columns_changes_test
test = pd.concat([X_test,Y_test],axis=1)

##Creating the features concatenation
features = "+".join(columns_changes)

##Creating Null and Full formula
var1 = columns_changes[0]  
null = 'OS_MONTHS ~' + var1
full = 'OS_MONTHS ~' + features

model           = stepwisereg(100,1)
model_fit       = model.fit(train,null,full,'OS_MONTHS')
model_param     = model_fit.params
test_predict    = model_fit.predict(test)
print(model_fit.summary())