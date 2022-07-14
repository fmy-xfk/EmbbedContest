import socket
import sys
import library.logger as logger
import numpy as np
from math import sin, cos, pi, sqrt

IP = '192.168.1.125' #固定的地址，不要改
PORT = 2368 #固定的端口，不要改
SCAN_TIMES = 80 #Ubuntu:120
TIME_OUT = 2 #超时设置，单位：秒
MAX_POINTS_CNT = 12 * SCAN_TIMES

def print_socket_info():
    logger.log("--------------------------------------")
    logger.log("IP: "+IP)
    logger.log("PORT: "+str(PORT))
    logger.log("SCAN_TIMES: "+str(SCAN_TIMES))
    logger.log("TIME OUT: "+str(TIME_OUT))
    logger.log("--------------------------------------")

print_socket_info()
server_cocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (IP, PORT)
server_cocket.bind(address)
server_cocket.settimeout(TIME_OUT) 

#接收原始数据
def __get_lidar_data():
    try:
        receive_data, client = server_cocket.recvfrom(1206) #old:1200
        return (receive_data[0:1200]).hex()
        '''receive_data, client = server_cocket.recvfrom(1200) #old:1200
        return (receive_data).hex()'''
    except socket.timeout:  #超时提示
        logger.log("Time out! Fail to get original data.",2)

#通信测试
def connection_test(limit):
    ret=None
    pf_cnt=0
    while(pf_cnt<limit and ret==None):
        ret=__get_lidar_data()
        pf_cnt+=1
    if(pf_cnt>=limit):
        return False
    else:
        return True

if not connection_test(5): 
    logger.log("Unbale to pass the connection test! Program will terminate.",3)

#直接返回点云
def get_points():
    x=[]
    y=[]
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                x.append(last_dis * cos(angle2 * pi / 180))
                y.append(last_dis * sin(angle2 * pi / 180))
            x.append(distance1 * cos(angle1 * pi / 180))
            y.append(distance1 * sin(angle1 * pi / 180))
            last_ang = angle1
    return [x, y]

def __get_sorted_data():
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    point_data = {}
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                point_data[angle2] = last_dis
            point_data[angle1] = distance1
            last_ang = angle1
    point_data = list(point_data.items())
    point_data = sorted(point_data,key=lambda x:x[0])
    return point_data

#返回排序后的点云
def get_sorted_points():
    x=[]
    y=[]
    cnt=0
    for i in range(SCAN_TIMES):
        data=None
        try:
            data, client = server_cocket.recvfrom(1206) #old:1200
        except socket.timeout:  #超时提示
            logger.log("Time out! Fail to get original data.",2)
            continue;
        for j in range(0,1200,100):
            #4+4+4+2+90+4+2+90
            ang = (data[j+2]+(data[j+3]<<8)) / 100
            dis = (data[j+4]+(data[j+5]<<8)) / 500
            if(cnt&1==1):
                x.append(dis * cos(ang * pi / 180))
                y.append(dis * sin(ang * pi / 180))
            cnt+=1
    return x,y
    
#返回排序后的点云
def get_sorted_points2():
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    point_data = {}
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                point_data[angle2] = last_dis
            point_data[angle1] = distance1
            last_ang = angle1
    point_data = list(point_data.items())
    x, y = [],[]
    st=sorted(point_data,key=lambda x:x[0])
    for angle, distance in st:
        x.append(distance * cos(angle * pi / 180))
        y.append(distance * sin(angle * pi / 180))
    return [x,y]
