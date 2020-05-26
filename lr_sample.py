#导包
import numpy as np
from sklearn import datasets , linear_model
from sklearn.metrics import mean_squared_error , r2_score
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import pdb

#加载糖尿病数据集
diabetes = datasets.load_diabetes()
pdb.set_trace()
X = diabetes.data[:,np.newaxis ,2] #diabetes.data[:,2].reshape(diabetes
#.data[:,2].size,1)
y = diabetes.target
X_train , X_test , y_train ,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
#导入模型，模型参数默认
LR = linear_model.LinearRegression()
#训练模型
LR.fit(X_train,y_train)
#预测模型LR.predict(X_test),此时输出类别数据
#打印截距
print('intercept_:%.3f' % LR.intercept_)
#打印模型系数
print('coef_:%.3f' % LR.coef_)
#打印均方误差值
print('Mean squared error: %.3f' % mean_squared_error(y_test,LR.predict(X_test)))##((y_test-LR.predict(X_test))**2).mean()
#打印R-平方
print('Variance score: %.3f' % r2_score(y_test,LR.predict(X_test)))
#1-((y_test-LR.predict(X_test))**2).sum()/((y_test - y_test.mean())**2).sum
#打印准确率accuracy
print('score: %.3f' % LR.score(X_test,y_test))
plt.scatter(X_test , y_test ,color ='green')
plt.plot(X_test ,LR.predict(X_test) ,color='red',linewidth =3)
plt.show()

