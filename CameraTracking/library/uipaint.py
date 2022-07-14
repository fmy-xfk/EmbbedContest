from matplotlib import pyplot as plt
import numpy as np

def pic_start():
    plt.ion()
    
def draw_points(points, color = 'b'):
    plt.scatter(np.array([p.x for p in points]), np.array([p.y for p in points]), c = color)

def pic_show():
    plt.show()
    plt.pause(0.02)
    plt.clf()

def draw_boundray(x, y, color = 'k'):
    plt.scatter(np.array(x),np.array(y), c=color, s=1)

def draw_area(points, color = 'r'):
    points.append(points[0])
    plt.plot(np.array([p.x for p in points]), np.array([p.y for p in points]), color)
