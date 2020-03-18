import SplineCurve
from Curvilinearcoord import curv2xy

# 测试：绘制三次样条曲线y=f(s),x=g(s)
import sys
import numpy as np
import matplotlib.pyplot as plt

fig2=plt.figure(figsize=(6,6))
ax2=fig2.add_subplot(1,1,1)
s = [-4,0,4,8,12,16,20,24];
x = [2.4,1.2,0.6,1.8,3,4.5,5.6,4.4];
y = [3.4,2.2,0.8,-1.2,-1.8,-0.4,1.7,2.3]
spline = SplineCurve.Spline(s,x)
spline2 = SplineCurve.Spline(s,y)
rs = np.arange(-4,30,0.01)
rx = [spline.calc(i) for i in rs]
ry = [spline2.calc(i) for i in rs]


curv = []
for i in range(len(rs)):
    curv.append([rs[i],rx[i],ry[i]])

#这里point曲线坐标
inputs=input("please input your value s(from -4 to 30):")
inputv=input("please input your value v(whatever):")
point = [float(inputs),float(inputv)]
pointxy = curv2xy(point,curv)
ppsd = [(i[0]-point[0])**2 for i in curv]
ps = ppsd.index(min(ppsd))

ppx = [pointxy[0],rx[ps]]
ppy = [pointxy[1],ry[ps]]

ax2.plot(pointxy[0],pointxy[1],"og")
ax2.plot(rx,ry,"-r")
if point[1]>=0:
    ax2.plot(ppx,ppy,"-b")
else:
    ax2.plot(ppx,ppy,"-g")
ax2.set_title("Red-baseline,green point-input point, the other line-vertical vector\n(green if v<0,blue if v>0)")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
#plt.plot(ppxpos,ppypos,"-g")
#plt.plot(ppxneg,ppyneg,"-y")
print(pointxy)
plt.show()