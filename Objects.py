# 定义障碍物，判断点是否在障碍物内
import math
def GetDot(p1, p2, p):
    return (p2[0] - p1[0]) * (p[0] - p1[0]) + (p2[1] - p1[1]) * (p[1] - p1[1])


def GetCross(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p[0] - p1[0]) * (p2[1] - p1[1])


def distance(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


class obstacle:
    def __init__(self, point1, point2, point3):  # 左上 右上 左下
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = [point2[0] + point3[0] - point1[0], point3[1] + point2[1] - point1[1]]
        self.center = [(point2[0] + point3[0]) / 2, (point3[1] + point2[1]) / 2]
        point4 = self.point4

        self.edge1 = [point2[0] - point1[0], point2[1] - point1[1]]
        self.edge2 = [point3[0] - point1[0], point3[1] - point1[1]]
        self.edge3 = [point4[0] - point3[0], point4[1] - point3[1]]
        self.edge4 = [point4[0] - point2[0], point4[1] - point2[1]]

    def inside(self, p):  # 判断一个外部点是不是在矩形里面
        return GetDot(self.point3, self.point1, p) >= 0 and GetDot(self.point3, self.point4, p) >= 0 and GetDot(
            self.point2, self.point4, p) >= 0 and GetDot(self.point2, self.point1, p) >= 0

