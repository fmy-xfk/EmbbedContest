import enum
import library.logger as logger
import library.uipaint as pd
import library.geometry as geo
from peripheral.camera import Camera
from library.geometry import get_middle_point, get_distance

MSG_NO_CAMERA="Camera wasn't assigned. Operation 'track_person' will not be executed."

class Identity(enum.Enum):
    student = 1
    teacher = 2

class Person():
    def __init__(self,identity, height=1.5,camera = None):
        self.count = 0
        self.cam = camera
        self.id = identity
        self.height = height
        self.position = []
        self.past_position = []

    def assign_new_camera(self, name, x,y,z, rotationAngle, cHor=10, cVer=10):
        self.cam = Camera(name, x,y,z, rotationAngle, camHorSpeed=cHor, camVerSpeed=cVer)

    def track_person(self, poe_index = -1):
        if(self.cam == None): 
            logger.log(MSG_NO_CAMERA,1)
            return
        if len(self.position) > 0:
            if not self.is_slight_shaking():
                p = self.position[poe_index]
                self.cam.position_control(p.x, p.y, self.height)

    def track_middle(self):
        if(self.cam == None): 
            logger.log(MSG_NO_CAMERA,1)
            return
        p = get_middle_point(self.position[0],self.position[-1])
        self.cam.position_control(p.x, p.y, self.height)

    def is_slight_shaking(self, distance = 0.05):
        if len(self.position) == len(self.past_position):
            for now, past in zip(self.position,self.past_position):
                if get_distance(now, past) < distance:
                    return True
        return False

    def add_count(self, add=1):
        self.count = self.count + add
    
    def reset_count(self):
        self.count = 0
        self.past_position = self.position[:]
        self.position = []

    def add_position(self, point):
        flag=True
        for i,p in enumerate(self.position):
            if(geo.get_distance(p,point)<0.3):
                self.position[i]=get_middle_point(p,point)
                flag=False
                break
        if(flag):
            self.count = self.count + 1
            self.position.append(point)

    def draw(self, color):
        pd.draw_points(self.position,color)

def check_identity(point, classroom):
    if classroom.is_teacher(point):
        return Identity.teacher
    elif classroom.is_student(point):
        return Identity.student
