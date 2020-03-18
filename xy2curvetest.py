import SplineCurve
from Curvilinearcoord import xy2curv

#测试：绘制三次样条曲线y=f(s),x=g(s)
import sys
import numpy as np
import matplotlib.pyplot as plt

fig1=plt.figure(figsize=(6,6))
ax1=fig1.add_subplot(1,1,1)
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

#这里point点坐标可以随便输
x=input("please input your x value(from 0 to 7):")
y=input("please input your y value(from -2 to 5):")
point = [float(x),float(y)]
pointcurv = xy2curv(point,curv)
fs = pointcurv[2]
vertical = pointcurv[1]
ppx = [point[0],rx[fs]]
ppy = [point[1],ry[fs]]

ax1.plot(point[0],point[1],"ob")
ax1.plot(rx,ry,"-r")
if vertical>=0:
    ax1.plot(ppx,ppy,"-b")
else:
    ax1.plot(ppx,ppy,"-g")
ax1.set_title("Red-baseline,blue point-input point, the other line-vertical vector\n(green if v<0,blue if v>0)")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
#plt.plot(ppxpos,ppypos,"-g")
#plt.plot(ppxneg,ppyneg,"-y")
print(pointcurv)

plt.show()