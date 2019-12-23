import numpy as np
import matplotlib.pyplot as plt

path00 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\1.9.txt"
path01 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\test1.9.txt"
path10 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\1.5.txt"
path11 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\test1.5.txt"
path20 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\1.3.txt"
path21 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\test1.3.txt"
path30 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\0.2_2.txt"
path31 = r"C:\Users\clair\Desktop\Lidar Project\Experiment\data\data\test0.2_2.txt"
data0 = np.loadtxt(path00)
data1 = np.loadtxt(path10)
data2 = np.loadtxt(path20)
data3 = np.loadtxt(path30)
fig = plt.figure(facecolor='None')
font = {'family' : 'Times New Roman','weight' : 'normal','size':17}
range_pt =  data0[:,0]
range_pt = range_pt.tolist()
num = np.loadtxt(path01)
group_mean = []
for count in range(len(num)):
    group_mean.append(sum(range_pt[0 : int(num[count])]) / len(range_pt[0 : int(num[count])]))
    del range_pt[0:int(num[count])]
ax1=fig.add_subplot(2,2,4)
ax1.scatter(group_mean,num)
ax1.set_title("EI4",font)
ax1.set_xlabel('Range (m)',font)
ax1.set_ylabel('PN',font)
z1 = np.polyfit(group_mean[-1:-(int(0.75*len(group_mean))):-1], num[-1:-(int(0.75*len(num))):-1],1)
p1 = np.poly1d(z1)
print(p1)
num_vals=p1(group_mean[-1:-(int(0.75*len(group_mean))):-1])
ax1.plot(group_mean[-1:-(int(0.75*len(group_mean))):-1],num_vals,"r",linewidth=2.2)

range_pt =  data1[:,0]
range_pt = range_pt.tolist()
num = np.loadtxt(path11)
group_mean = []
for count in range(len(num)):
    group_mean.append(sum(range_pt[0 : int(num[count])]) / len(range_pt[0 : int(num[count])]))
    del range_pt[0:int(num[count])]
ax2=fig.add_subplot(2,2,3)
ax2.scatter(group_mean,num)
ax2.set_title("EI3(OD1.5)",font)
ax2.set_xlabel('Range (m)',font)
ax2.set_ylabel('PN',font)
z2 = np.polyfit(group_mean[-1:-(int(0.6*len(group_mean))):-1], num[-1:-(int(0.6*len(num))):-1],1)
p2 = np.poly1d(z2)
print(p2)
num_vals=p2(group_mean[-1:-(int(0.6*len(group_mean))):-1])
ax2.plot(group_mean[-1:-(int(0.6*len(group_mean))):-1],num_vals,"r",linewidth=2.2)

range_pt =  data2[:,0]
range_pt = range_pt.tolist()
num = np.loadtxt(path21)
group_mean = []
for count in range(len(num)):
    group_mean.append(sum(range_pt[0 : int(num[count])]) / len(range_pt[0 : int(num[count])]))
    del range_pt[0:int(num[count])]
ax3=fig.add_subplot(2,2,2)
ax3.scatter(group_mean,num)
ax3.set_title("EI3(OD1.3)",font)
ax3.set_xlabel('Range (m)',font)
ax3.set_ylabel('PN',font)
z3 = np.polyfit(group_mean[-1:-(int(0.5*len(group_mean))):-1], num[-1:-(int(0.5*len(num))):-1],2)
p3 = np.poly1d(z3)
print(p3)
num_vals=p3(group_mean[-1:-(int(0.5*len(group_mean))):-1])
ax3.plot(group_mean[-1:-(int(0.5*len(group_mean))):-1],num_vals,"r",linewidth=2.2)

range_pt =  data3[:,0]
range_pt = range_pt.tolist()
num = np.loadtxt(path31)
group_mean = []
for count in range(len(num)):
    group_mean.append(sum(range_pt[0 : int(num[count])]) / len(range_pt[0 : int(num[count])]))
    del range_pt[0:int(num[count])]
ax4=fig.add_subplot(2,2,1)
ax4.scatter(group_mean,num)
ax4.set_title("EI1 & EI2",font)
ax4.set_xlabel('Range (m)',font)
ax4.set_ylabel('PN',font)
#z4 = np.polyfit(group_mean[-1:-(int(0.5*len(group_mean))):-1], num[-1:-(int(0.5*len(num))):-1],2)
#p4 = np.poly1d(z4)
#print(p3)
#num_vals=p4(group_mean[-1:-(int(0.5*len(group_mean))):-1])
#ax4.plot(group_mean[-1:-(int(0.5*len(group_mean))):-1])
plt.ylim(0,25)
plt.subplots_adjust(left=0.1,bottom=0.1,right=0.97,top=0.95,wspace=0.2,hspace=0.4)
plt.show()
savepath = r"C:\Users\clair\Desktop\Thesis\fig\ "
fig.savefig(savepath+"pt_num_fit.png")