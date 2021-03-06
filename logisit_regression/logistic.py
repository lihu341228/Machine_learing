import pandas as pd

filename = 'bankloan.xls'
data = pd.read_excel(filename)
x = data.iloc[:, :8].as_matrix()
y = data.iloc[:, 8].as_matrix()



from sklearn.linear_model import LogisticRegression as LR
from sklearn.linear_model import RandomizedLogisticRegression as RLR

rlr=RLR()
rlr.fit(x,y)
rlr.fit(x,y)
rlr.get_support()
print("end search useful_data")
print(u'end search useful data: %s'%''.join(data.columns[rlr.get_support()]))

x = data[data.columns[rlr.get_support()]].as_matrix()

lr = LR()
lr.fit(x, y)
print()
print('%s'% lr.score(x, y))