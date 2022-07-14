from peripheral.lslidar import get_points
import numpy as np
from matplotlib import pyplot as plt
import library.file as fileop
import sys
import tkinter as tk

#filename=""
save = True
view = True
no_exit = True
xd,yd=[],[]
x,y=[],[]

def draw_once(get_new_data = True):
    global x,y
    if(get_new_data or x==[] or y==[]): x, y = get_points()  
    plt.scatter(np.array(x),np.array(y))
    plt.scatter(0,0, c = 'r',marker='x')

def on_paint():
    plt.clf()
    draw_once()
    if view and len(xd)!=0:
        plt.plot(np.array(xd),np.array(yd),'r')
        plt.scatter(xd[-1],yd[-1])
    else:
        plt.scatter(np.array(xd),np.array(yd), c = 'r')
    plt.ion()

def on_mouse_click(event):
    global filename
    if event.button == 1: #Left button
        xd.append(event.xdata)
        yd.append(event.ydata)            
    elif event.button == 3: #Right button
        xd.clear()
        yd.clear()
    '''elif event.button == 2: #Middle button
        if filename != areas['sh']:
            global view
            view = not view
        else:
            with open(filename,'a',encoding = 'utf-8') as f:
                f.write('next\n')
                xd.clear()
                yd.clear()'''
    on_paint()

def on_key_press(event):
    global no_exit,save
    if(event.key=="escape"): 
        no_exit = False
        save = False
    elif(event.key=='r' or event.key=='R'):
        on_paint()
    elif(event.key=='enter' or event.key=='R'):
        no_exit = False
        save = True

def on_form_closing(event):
    global no_exit,save
    no_exit = False
    save=True

def  start_draw(fname):
    global xd,yd,no_exit,save
    no_exit=True
    plt.close('all')

    filename=fname
    points = fileop.read_points(filename)
    xd, yd = [p[0] for p in points], [p[1] for p in points]
    
    fig = plt.figure()
    fig.canvas.mpl_connect('button_press_event',on_mouse_click)
    fig.canvas.mpl_connect('key_press_event',on_key_press)
    fig.canvas.mpl_connect('close_event',on_form_closing)  
    #plt.ion()
    plt.gca().set_aspect(1)

    on_paint()

    while no_exit:
        plt.pause(0.02)
    
    if save:
        fileop.write_points(filename,zip(xd,yd))
    
    del fig
    sys.exit()
    

def on_butB_click():
   start_draw('area/boundary.txt')

def on_butS_click():
    start_draw('area/student.txt')

def on_butT_click():
    start_draw('area/teacher.txt')

def on_butSH_click():
    start_draw('area/shield.txt')

def gen_window():
    dfont=("宋体",11)
    W=tk.Tk()
    W.title("区域编辑器")
    W.geometry("400x300")
    tk.Label(W,text="请选择要编辑的区域：",font=("宋体",18)).place(x=10,y=10)
    tk.Button(W,text="边界",font=dfont,command=on_butB_click).place(x=10,y=50)
    tk.Button(W,text="学生区",font=dfont,command=on_butS_click).place(x=70,y=50)
    tk.Button(W,text="教师区",font=dfont,command=on_butT_click).place(x=150,y=50)
    tk.Button(W,text="屏蔽区",font=dfont,command=on_butSH_click).place(x=230,y=50)
    tk.Label(W,text="提示：",font=dfont).place(x=10,y=90)
    tk.Label(W,text="按Esc键不保存退出，按Enter键保存并退出，按R键刷新",font=dfont).place(x=10,y=120)
    tk.Label(W,text="鼠标左键单击选择边界点，右键单击重设边界点",font=dfont).place(x=10,y=150)
    tk.mainloop()

if __name__=="__main__":
    gen_window()
