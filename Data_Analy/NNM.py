import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn import svm
import pickle
from sklearn.externals import joblib

data00=np.loadtxt(r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt\OD_2edclass.txt")
Y=data00[:,4]
Y=Y.astype('int')
X=data00[:,0:4]
X_train, X_test, Y_train, Y_test=train_test_split(X, Y, test_size=0.33)
scaler = StandardScaler()
scaler.fit(X_train)
#scal = open(r'C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt+field\scal0.txt','wb')
#pickle.dump(scaler,scal)
#scal.close()
#joblib.dump(scaler, r'C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt+field\scal0.model')
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
clf=MLPClassifier()#early_stopping=True,learning_rate_init=0.01,hidden_layer_sizes=(100,20))
clf.fit(X_train,Y_train)
Y_pred=clf.predict(X_test)
print(clf,clf.n_iter_,clf.n_layers_)
print(classification_report(Y_test,Y_pred))#target_names=[0.8,1.5,1.9]
clf2 = svm.SVC()
clf2.fit(X_train,Y_train)
Y_pred=clf2.predict(X_test)
print(classification_report(Y_test,Y_pred))
#fw = open(r'C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt+field\clf0.txt','wb')
#pickle.dump(clf,fw)
#fw.close()
#joblib.dump(clf, r'C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt+field\clf0.model')
#fw = open(r'C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt+field\clf0_svc.txt','wb')
#pickle.dump(clf2,fw)
#fw.close()
#joblib.dump(clf2, r'C:\Users\clair\Desktop\Lidar Project\Experiment\data\add_pt+field\clf0_svc.model')
# data5=np.loadtxt("data5.txt")
# data6=np.loadtxt("data6.txt")
# data7=np.loadtxt("data7.txt")
# data01=np.vstack([data5,data6,data7])
# X_test2=data01[:,1:3]
# Y_test2=data01[:,4]*10
# Y_test2=Y_test2.astype('int')
# Y_pred_test=clf.predict(X_test2)
# print(classification_report(Y_test2,Y_pred_test))
# for i in range(len(data00)-1):
#     if int(data00[i,4])==2:
#         data00[i,4]=0
#     elif int(data00[i,4])==8:
#         data00[i,4]=6
#     elif int(data00[i,4])==15:
#         data00[i,4]=13
#     elif int(data00[i,4])==19:
#         data00[i,4]=19
#
# # data00=np.vstack([data2,data3,data4])