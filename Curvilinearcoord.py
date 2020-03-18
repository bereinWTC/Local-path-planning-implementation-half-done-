# function：曲线坐标/直角坐标相互转换
from scipy.spatial.distance import pdist
import math
import numpy as np


# 曲线给定，输入(x,y),输出(s,v)，以v绝对值最小为原则。
def xy2curv(point, curv):
    # 求坐标的函数，首先根据最小距离得到s坐标和v坐标的绝对值
    distances = []
    rrs = [i[0] for i in curv]
    rrx = [i[1] for i in curv]
    rry = [i[2] for i in curv]
    for i in range(len(curv)):
        X = np.vstack([point, [rrx[i], rry[i]]])
        distances.append(pdist(X)[0])
    fs = distances.index(min(distances))
    vertical = min(distances)

    # 判断vertical正负，根据s坐标计算出法向量
    dxdy = [rrx[fs + 1] - rrx[fs], rry[fs + 1] - rry[fs]]
    # 先把求到的dxdy求单位值
    norm = 0
    for i in range(len(dxdy)):
        norm += dxdy[i] ** 2
    for i in range(len(dxdy)):
        dxdy[i] = dxdy[i] / math.sqrt(norm)

    # 求dxdy法向量
    vert = [-dxdy[1], dxdy[0]]  # 沿s行走逆时针为正 - 这个是法向量

    # 和法向量求数量积
    lxly = [point[0] - rrx[fs], point[1] - rry[fs]]
    quad = lxly[0] * vert[0] + lxly[1] * vert[1]
    # 根据数量积的正负值，判断v的正负
    if quad >= 0:
        vertical = vertical
    else:
        vertical = -vertical

    return [rrs[fs], vertical, fs]

    # 然后根据距离计算出正负点
    # disver = [i*vertical for i in posdxdy]
    # pointpos = [rx[fs]+dispos[0],ry[fs]+dispos[1]]


# 曲线给定，输入（s,v）输出（x,y），在任意赋值时，可能会有多组（s，v）对应到同一个（x,y）
def curv2xy(point, curv):
    s = point[0]
    v = point[1]
    #先把乌七八糟的情况去掉
    if v == None:
        return None

    rrs = [i[0] for i in curv]
    rrx = [i[1] for i in curv]
    rry = [i[2] for i in curv]
    # 首先根据输入的s值找到他在曲线中对应的字典位置
    rrsd = [(i[0] - s) ** 2 for i in curv]
    #这里也把乌七八糟的情况去掉，离开路径太远的点不予计算
    if s < rrs[0]:
        return None
    elif s > rrs[-1]:
        return None
    fs = rrsd.index(min(rrsd))

    # 然后求出法向量
    dxdy = [rrx[fs + 1] - rrx[fs], rry[fs + 1] - rry[fs]]
    # 先把求到的dxdy求单位值
    norm = 0
    for i in range(len(dxdy)):
        norm += dxdy[i] ** 2
    for i in range(len(dxdy)):
        dxdy[i] = dxdy[i] / math.sqrt(norm)
    vert = [-dxdy[1], dxdy[0]]  # 法向量

    # 根据法向量求出距离
    disvert = [i * v for i in vert]
    x = rrx[fs] + disvert[0]
    y = rry[fs] + disvert[1]
    return [x, y]

