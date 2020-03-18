import SplineCurve
from Curvilinearcoord import xy2curv,curv2xy
from Objects import GetCross,GetDot,distance,obstacle
#测试：绘制三次样条曲线y=f(s),x=g(s)
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
import math

#建立一个路线，确定函数x=f1(s),y=f2(s), f1,f2为三次函数

s = [-4,0,4,8,12,16,20,24];
x = [2.4,1.2,0.6,1.8,3,4.5,5.6,4.4];
y = [3.4,2.2,0.8,-1.2,-1.8,-0.4,1.7,2.3]
spline = SplineCurve.Spline(s,x)
spline2 = SplineCurve.Spline(s,y)
rs = np.arange(-4,30,0.01)
rx = [spline.calc(i) for i in rs]
ry = [spline2.calc(i) for i in rs]

# 轨迹生成测试
# 设定v的范围（基本含义是路的宽度）
vmin = -0.6
vmax = 0.6
vrange = np.arange(vmin, vmax, 0.1)

# 下面这些列表是存变量用的
traces = []
tracess = []
tracesv = []
blockornot = []
curvs = []

# 创建一个障碍物
p1 = [7, 0.3]
p2 = [9, 0.3]
p3 = [7, -0.03]
blocker = obstacle(p1, p2, p3)
blockerx = [blocker.point1[0], blocker.point2[0], blocker.point4[0], blocker.point3[0], blocker.point1[0]]
blockery = [blocker.point1[1], blocker.point2[1], blocker.point4[1], blocker.point3[1], blocker.point1[1]]

# 创建一个车辆
cars=input("pleast input the s value of the car(between -4 and 14):")
carv=input("pleast input the v value of the car(between -0.6 and 0.6):")
point1 = (float(cars), float(carv))
print("Processing...please wait")
for i in vrange:
    point2 = (point1[0] + 5, i)
    theta = 0
    s2 = [point1[0], point2[0]]
    v2 = [point1[1], point2[1]]

    # 首先生成轨迹
    splineq = SplineCurve.Spline2Points(point1, point2, theta)
    #splines.append(splineq)
    rs3 = np.arange(point1[0],point1[0]+15, 0.01)
    rv3 = [splineq.calc(i) for i in rs3]
    tracess.append(rs3)
    tracesv.append(rv3)
    blocked = 0

    # 然后判定轨迹是否被挡
    for j in range(len(rs3)):
        pointtst = [rs3[j], rv3[j]]
        if blocker.inside(pointtst):
            blocked = 1
    blockornot.append(blocked)

    # 然后算轨迹总长度/s变化量
    points2 = []
    distancetotal = 0
    for j in range(len(rs3)):
        point = [rs3[j], rv3[j]]
        points2.append(point)
        if j != 0:
            distancetotal += distance(points2[j], points2[j - 1])
    curvvalue = distancetotal / (rs3[-1] - rs3[0])
    curvs.append(curvvalue)

    trace = {'id': i, 's': rs3, 'v': rv3, 'status': blocked, 'valeur': curvvalue}
    traces.append(trace)

curvsforchoice = curvs
for i in range(len(traces)):
    if blockornot[i] == 1:
        curvsforchoice[i] += max(curvsforchoice)
idchosen = curvsforchoice.index(min(curvsforchoice))
traces[idchosen]['status'] = 2
blockornot[idchosen] = 2

fig3=plt.figure(figsize=(6,6))
ax3=fig3.add_subplot(1,2,1)

for trace in traces:
    if trace['status'] == 1:
        ax3.plot(trace['s'], trace['v'], "-r")
    elif trace['status'] == 0:
        ax3.plot(trace['s'], trace['v'], "-y")
    else:
        ax3.plot(trace['s'], trace['v'], "-g")
    ax3.grid(True)

ax3.set_title("Path selection in curvilinear coordinates\n"
              "green for chosen path, yellow for available,\n"
              "red for blocked, black for obstacle")
ax3.plot(blockerx, blockery, "-k")
ax3.set_xlabel("s")
ax3.set_ylabel("v")

curv=[]
for i in range(len(rs)):
    curv.append([rs[i],rx[i],ry[i]])
p1xy = curv2xy(p1, curv)
p2xy = curv2xy(p2, curv)
p3xy = curv2xy(p3, curv)
blockerxy = obstacle(p1xy, p2xy, p3xy)
blockerx2 = [blockerxy.point1[0], blockerxy.point2[0], blockerxy.point4[0], blockerxy.point3[0], blockerxy.point1[0]]
blockery2 = [blockerxy.point1[1], blockerxy.point2[1], blockerxy.point4[1], blockerxy.point3[1], blockerxy.point1[1]]

ax4 = fig3.add_subplot(1, 2, 2)
ax4.set_title("Path selection in Catresian coordinates\n"
              "Blue for baseline, green for chosen path,\n"
              " yellow for available,red for blocked, black for obstacle")
for trace in traces:
    sbunch = trace['s']
    vbunch = trace['v']
    rx3 = []
    ry3 = []
    points3 = []
    for k in range(len(sbunch)):
        point = [sbunch[k], vbunch[k]]
        points3.append(point)
    for j in range(len(points3)):
        pointxy = curv2xy(points3[j], curv)
        if pointxy != None:
            rx3.append(pointxy[0])
            ry3.append(pointxy[1])
    if trace['status'] == 1:
        ax4.plot(rx3, ry3, "-r")
    elif trace['status'] == 0:
        ax4.plot(rx3, ry3, "-y")
    else:
        ax4.plot(rx3, ry3, "-g")
    ax4.grid(True)

ax4.plot(rx, ry, "-b")
ax4.plot(blockerx2, blockery2, "-k")
ax4.set_xlabel("x")
ax4.set_ylabel("y")
plt.show()
