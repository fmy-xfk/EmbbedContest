import library.logger as logger
import library.geometry as geo

def get_rect(points):
    xd=[p[0] for p in points]
    x=min(xd);width=max(xd)-x
    yd=[p[1] for p in points]
    y=min(yd);height=max(yd)-y
    return geo.Rect(x,y,width,height)

def get_area(filename):
    return get_rect(read_points(filename))    

def get_shields(filename):
    shields = []
    with open(filename,'r',encoding = 'utf-8') as f:
        sh = []
        for line in f.readlines():
            if line == 'next' and len(sh)>0:
                shields.append(get_rect(sh))
                sh.clear()
            elif line != '\n':
                x,y = line.split(',')
                sh.append([float(x),float(y)])
    if len(sh)>0:
        shields.append(get_rect(sh))
    return shields

def read_points(filename): 
    points = []
    try:
        f=open(filename,'r',encoding = 'utf-8')
        for line in f.readlines():
            if line != '\n':
                x,y = line.split(',')
                points.append([float(x),float(y)])
        f.close()
    except IOError:
        logger.log("Fail to read from "+filename,2)
    return points

def write_points(filename,points): 
    try:
        f=open(filename,'w',encoding = 'utf-8')
        for p in points:
            f.write("{0},{1}\n".format(str(p[0]),str(p[1])))
        f.close()
        return True
    except IOError:
        logger.log("Fail to write to "+filename,2)
        return False
