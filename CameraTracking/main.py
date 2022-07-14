from library.person import *
import library.geometry as geo
import library.uipaint as pd
import library.file as fileop
import library.logger as logger
from peripheral import *

DEBUG = True
points_resolution = 0.01
person_width = 0.3
boundary = fileop.get_area('area/boundary.txt')
tea_area = fileop.get_area('area/teacher.txt')
stu_area = fileop.get_area('area/student.txt')
#shield = fileop.get_shields('area/shield.txt')
classroom = geo.Map(student=stu_area, teacher=tea_area)

stu = Person(Identity.student,1.7,Camera('/dev/ttyUSB0',0.1, 0.4, 1, 0)) #Not precise: port, x, y, z, angle
tea = Person(Identity.teacher,1.5,Camera('/dev/ttyUSB1',0, 2, 1.8, 0))
#dis = Displayer('/dev/ttyUSB2')
pd.pic_start()

while True:
    x, y = get_sorted_points()
    if DEBUG:
        pd.plt.gca().set_aspect(1)
        classroom.draw()
        pd.draw_boundray(x,y)
    #pd.draw_points([geo.Point()])

    points = [geo.Point(x0, y0) for x0, y0 in zip(x,y)]
    plen = len(points)

    for p in points:
        if(classroom.is_student(p)): stu.add_position(p)
        if(classroom.is_teacher(p)): tea.add_position(p)

    #画坐标点
    if DEBUG:
        stu.draw('r')
        tea.draw('b')
    logger.log('stu={}\ttea={}'.format(stu.count,tea.count))
        
    #摄像头
    stu.track_person()
    tea.track_person()

    #屏幕
    #dis.update(stu.count, tea.count)

    stu.reset_count()
    tea.reset_count()
    if DEBUG:
        pd.pic_show()
