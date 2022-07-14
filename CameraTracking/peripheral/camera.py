import math
import serial
import library.logger as logger
from library.geometry import Point

#摄像头与人之间的距离，根据此来调节焦距(可能有错)
Focus_adjustment_ratio = [0x0000, 0x1606, 0x2151, 0x2860, 0x2cb5, 0x3060, 0x32d3, 0x3545, 0x3727, 0x38a9, 0x3a42, 0x3b4b, 0x3c85, 0x3d75, 0x3e4e, 0x3ef7, 0x3fa0, 0x4000]

#查询云台位置指令
Query_the_position_of_camera_pan_tilt= [0x81,0x09,0x06,0x12,0xff]

#打开电源指令{0x81,0x01,0x04,0x00,0x02,0xff}，关闭电源指令{0x81,0x01,0x04,0x00,0x03,0xff}
Power_control_command= [0x81,0x01,0x04,0x00,0x02,0xff]

#焦距参数0000为最远（OX00 00 00 00），03FF为最近（0X00 03 0F 0F）
Auto_focus= [0x81,0x01,0x04,0x38,0x02,0xff]#自动聚焦
Back_to_the_origin= [0x81,0x01,0x06,0x04,0xff]#----回到原点
Reset_camera = [0x81, 0x01, 0x06, 0x05, 0xff]#----复位
Change_focus = [0x81, 0x01, 0x04, 0x47, 0x00, 0x00, 0x00, 0x00, 0xff]#//----变焦

#云台控制的绝对位置控制
Absolute_position_control = [0x81, 0x01, 0x06, 0x02, 0x14, 0x14, 0x0F, 0x07, 0x02, 0x05, 0x00, 0x04, 0x0B, 0x00, 0xff]

'''
水平角度设置值：1（1.05 ）  2（2.12）   3（3.75）   4（4.37）   5（5.37）   6（6.43）   7（8.06）   8（10.25）   9（12.37）   10（12.37）  11（18.00）  12（21.25）  13（24.31）
单位度/秒     14（28.31） 15（32.31） 16（36.50） 17（41.18） 18（46.18） 19（51.25） 20（55.50） 21（66.81）  22（71.12）  23（75.99）  24（79.99）
'''

class Camera():
    def __init__(self,name,x,y,z, rotationAngle = 0, camHorSpeed=10, camVerSpeed=10):
        self.x, self.y, self.z = x, y, z
        self.hor_speed, self.ver_speed = camHorSpeed, camVerSpeed
        self.ro = rotationAngle
        self.port_name=name
        try:
            portx = name
            bps = 9600
            timex = 5
            self.ser = serial.Serial(portx,bps,timeout=timex)
        except Exception as e:
            self.ser = None
            logger.log("Can't open port " + name + str(e))

    def __angle_to_cmd(angle):
        #a = 0.075
        return ((int(angle/0.075) + 0x10000) & 0x0ffff)

    def __write(self, data):
        if(self.ser != None):
            return self.ser.write(bytearray(data))
        return 0

    def position_control(self, x, y, height=1.5):
        cmd = Absolute_position_control[:]
        cmd[4] = self.hor_speed
        cmd[5] = self.ver_speed
        p = Point(x-self.x, y-self.y, height-self.z)
        p.turn_to_polar()
        #hor = self.__angle_to_cmd(p.theta + self.ro)
        #ver = self.__angle_to_cmd(math.atan2(math.atan2(p.z, math.sqrt(p.x**2 + p.y**2))))
        hor = p.theta*180/math.pi + self.ro
        hor = (int(hor/0.075) + 0x10000) & 0x0ffff
        ver = math.atan2(p.z, math.sqrt(p.x**2 + p.y**2))*180/math.pi
        ver = (int(ver/0.075) + 0x10000) & 0x0ffff

        cmd[13] = ver & 0x000f
        cmd[12] = (ver >> 4) & 0x000f
        cmd[11] = (ver >> 8) & 0x000f
        cmd[10] = (ver >> 12) & 0x000f

        cmd[9] = hor & 0x000f
        cmd[8] = (hor >> 4) & 0x000f
        cmd[7] = (hor >> 8) & 0x000f
        cmd[6] = (hor >> 12) & 0x000f
        self.__write(cmd)
        if self.port_name!='':
            logger.log("Camera " + self.port_name + " rotated.")
        else:
            logger.log("A unnamed camera rotated.")

