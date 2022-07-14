# 运行程序说明
1. main.py
    录播系统主程序

2. devide.py
    区域划分程序
    运行后，输入‘b','s','t','sh'，分别进行边界、学生、老师、屏蔽区域的划分
    划分后的区域顶点坐标保存在文件夹area下对应的txt文件中

# 其他程序说明
1. lslidar.py
    读取雷达数据，以列表形式返回直角坐标系点云。
    数据格式：[[x0,x1,x2...],[y0,y1,y2...]]

    `__get_lidar_data()`：通过网口获取雷达原始二进制数据

    `get_points()`：返回直角坐标点云

    `get_sort_points()`：返回按0-360排序后的直角坐标点云

2. point_map.py
    处理坐标点相关

    1. 类：
        1. `Point`
        2. `Area`
        3. `Map`

    2. 函数
        1. `comput_distance(p1, p2)`
            返回p1和p2在xy平面上的距离
        
        2. `call_middle_point(p1, p2)`
            返回p1和p2的中点

        3. `is_equal(p1, p2)`
            判断p1和p2是否为同一个点

3. person.py
    1. Person类说明
        记录并处理检测到的人的坐标等信息

    2. 类方法说明
        1. 


4. picture_draw.py

5. readfile.py
    读取文件，返回文件里的数据
    1. `get_area(filename)`
        读取
            边界：area/boundary.txt
            学生区：area/student.txt
            教师区：area/teacher.txt
        数据返回格式：返回各个顶点坐标列表的列表
        [[顶点1x, 顶点1y], [顶点2x, 顶点2y], ...]
    
    2. `get_shields(filename)`
        读取文件area/shield.txt,返回包含多个屏蔽区的列表

6. displayer.py

7. camera_control.py
