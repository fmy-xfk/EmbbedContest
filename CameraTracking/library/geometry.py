import numpy as np
import library.logger as logger
import math
import library.uipaint as pd

class Point():
    def __init__(self, x=0, y=0, z=0, rh=None, theta=None):
        self.z = z
        self.rh, self.theta = rh, theta
        if rh == None:
            self.x, self.y = x,y
            self.theta = math.atan2(self.y,self.x)
            self.rh = math.sqrt(self.x**2 + self.y**2)
        else:          
            self.x = rh * math.cos(theta)
            self.y = rh * math.sin(theta)

    def turn_to_polar(self):
        self.theta = math.atan2(self.y,self.x)
        self.rh = math.sqrt(self.x**2 + self.y**2)

    def get_distance(self, point):
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)

    def get_middle_point(self,point):
        return Point((self.x+point.x)/2, (self.y+point.y)/2)

    def get_turn_angle(self,from_,to):
        p1 = Point(from_.x-self.x, from_.y - self.y)
        p2 = Point(to.x-self.x, to.y - self.y)
        result = p2.theta - p1.theta
        while math.fabs(result) > math.pi:
            if result>0:
                result -= 2*math.pi
            else:
                result += 2*math.pi
        return result

    def equal_to(self, point):
        return self.x == point.x and self.y == point.y

class Line():
    def __init__(self, p1, p2):
        self.point1, self.point2 = p1, p2
        self.a, self.b = solve(np.array([[p1.x,1],[p2.x,1]]), np.array([p1.y,p2.y]))

    def get_distance(self, point):
        dis = ((self.a * point.x - point.y + self.b)**2) / (self.a**2+1)
        return math.sqrt(dis)

class Rect():
    def __init__(self,x,y,width,height):
        self.x,self.y,self.width,self.height=x,y,width,height
    def contains(self,p):
        x,y,width,height=self.x,self.y,self.width,self.height
        return p.x>self.x and p.x<x+width and p.y<y+height and p.y>y
    def draw(self, color):
        x,y,width,height=self.x,self.y,self.width,self.height
        pd.draw_area([Point(x,y),Point(x+width,y),Point(x+width,y+height),Point(x,y+height),Point(x,y)],color)

class Map():
    def __init__(self, student, teacher, shields=[]):
        self.stu = student
        self.tea = teacher
        self.shields = []
        for shield in shields:
            self.shields.append(shield)
            
    def is_not_in_shields(self,point):
        for shield in self.shields:
            if(not shield.contains(point)): return False
        return True
    
    def is_teacher(self, point):
        return self.tea.contains(point)

    def is_student(self, point):
        return self.stu.contains(point)

    def draw(self):
        self.stu.draw('y')
        self.tea.draw('k')
        #for sh in self.shields:
        #    sh.draw('g')

def get_distance(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

def get_middle_point(p1, p2):
    return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

def is_equal(p1, p2):
    return p1.x == p2.x and p1.y == p2.y
