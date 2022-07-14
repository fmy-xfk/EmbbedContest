import serial
import library.logger as logger
from enum import Enum

#输出 Student给录播主机，捕获学生起立运动，发出“FF 02 00 07 00 50 59”
student_Close_up_camera = [0xff,0x02,0x00,0x07,0x00,0x50,0x59]
student_all = [0xff,0x01,0x04,0x0a,0x0a]
teacher_Close_up_camera = [0xff,0x01,0x00,0x07,0x00,0x50,0x58]
teacher_all = [0xff,0x01,0x04,0x0b,0x0b]

class Scene(Enum):
    teacher_all = 1
    student_all = 2
    teacher_feature = 3
    student_feature = 4

class Displayer():
    def __init__(self, name):
        self.current_display = Scene.student_all
        self.wait_flag = True
        try:
            portx = name
            bps = 9600
            timex = 5
            self.ser = serial.Serial(portx, bps, timeout=timex)
            logger.log("Displayer initialized.")
        except Exception as e:
            logger.log("Can't open port " + name+"\n"+str(e),2)
        
    def __change(self,display):
        if display == Scene.student_all:
            self.__write(student_all)
        elif display == Scene.student_feature:
            self.__write(student_Close_up_camera)
        elif display == Scene.teacher_all:
            self.__write(teacher_all)
        elif display == Scene.teacher_feature:
            self.__write(teacher_Close_up_camera)
        logger.log("Displayer has been changed to "+str(display))

    def update(self, stu, tea):
        if stu == 1:
            dis = Scene.student_feature
        elif stu > 1:
            dis = Scene.student_all
        else:
            if tea == 0:
                dis = Scene.student_all
            elif tea == 1:
                dis = Scene.teacher_feature
            else:
                dis = Scene.teacher_all
        
        if self.current_display != dis:
            self.current_display = dis 
            self.__change(dis)

    def __write(self, data):
        return self.ser.write(bytearray(data))
