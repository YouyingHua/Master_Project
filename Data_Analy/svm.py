import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn import svm

path0=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD0.txt"
path1=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD0.2.txt"
path2=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD0.6.txt"
path3=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD0.8.txt"
path4=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD1.3.txt"
path5=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD1.5.txt"
path6=r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\lslidar1\OD1.9.txt"
from sklearn.externals import joblib

data0 = np.loadtxt(path0)
data1 = np.loadtxt(path1)
data2 = np.loadtxt(path2)
data3 = np.loadtxt(path3)
data4 = np.loadtxt(path4)
data5 = np.loadtxt(path5)
data6 = np.loadtxt(path6)
y0 = [0]*(len(data0)+len(data1))
y1 = [1]*len(data1)
y2 = [2]*(len(data2)+len(data3))
y3 = [3]*len(data3)
y4 = [4]*(len(data4)+len(data5))
y5 = [5]*len(data5)
y6 = [6]*len(data6)
Y = y0+y2+y4+y6
data = np.vstack([data0,data1,data2,data3,data4,data5,data6])
print(np.shape(data))
print(np.shape(Y))

R = data[:,0]
I = data[:,1]
X_train, X_test, Y_train, Y_test=train_test_split(data[:,0:4], Y, test_size=0.33)
#clf=MLPClassifier()
clf = svm.SVC()
clf.fit(X_train,Y_train)
Y_pred=clf.predict(X_test)
print(classification_report(Y_test,Y_pred))
joblib.dump(clf, 'four_group.model')