#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Int8
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Point
import time
import os

import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import PIL.Image
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import cv2                      # used to change the color channel in the photo
#from tkFont import Font



LARGE_FONT=("Verdana",14)
style.use("dark_background")

start_not_stop = 0
#array where the coordinates of the Point cloud will be stored
xList = []					
yList = []
zList = []
# array to store the coordinates on the left photo
xList_L = []
yList_L = []
# array to store the coordinates on the right photo
xList_R = []
yList_R = []

N = 0

# Point cloud plot
f = plt.figure(figsize=(9,6.5))
a = plt.subplot()
plt.ion()

# left plot
f_left = plt.figure(figsize = (5.5,3))
a_left= plt.subplot()

# right plot
f_right = plt.figure(figsize = (5.5,3))
a_right = plt.subplot()




def change_state_start():

    # loads the initial images taken with lights on 
    path_left = '/home/lidart/init_photos/left/left_init.png'
    path_right = '/home/lidart/init_photos/right/right_init.png'
    # left 
    img_left = plt.imread(path_left)
    #opencv uses BGR and matplotlib uses RGB
    img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB)
    a_left.imshow(img_left)

    # right
    img_right = plt.imread(path_right)
    img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB)
    a_right.imshow(img_right)


    start_not_stop = 1
    # Deactivate entries when the system is working
    opFoVh.config(state='disabled')
    opFoVv.config(state='disabled')
    opsteph.config(state='disabled')
    opstepv.config(state='disabled')

    global FoVh, FoVv, stepv, steph, N

    FoVh = int(10000*float(opFoVh.get()))
    if FoVh > 450000:                                   # If the input horizontal field of view is bigger than the maximum (45 degress), then the maximum is assumed
        FoVh = 450000
    if FoVh < 3:                                        # If the input horizontal field of view is less than the minimum (the minimum step possible), then the minimum is assumed
        FoVh = 3

    FoVv = int(10000*float(opFoVv.get()))
    if FoVv > 450000:                                   # If the input vertical field of view is bigger than the maximum (45 degress), then the maximum is assumed
        FoVv = 450000
    if FoVv < 3:                                        # If the input vertical field of view is less than the minimum (the minimum step possible), then the minimum is assumed
        FoVv = 3

    steph = int(10000*float(opsteph.get()))
    if steph > FoVh:                                    # If the input horizontal step is bigger than the maximum (the horizontal FoV), then the maximum is assumed
        steph = FoVh
    if steph < 3:                                       # If the input horizontal step is less than the minimum achievable by the system (), then the minimum is assumed
        steph = 3

    stepv = int(10000*float(opstepv.get()))
    if stepv > FoVv:                                    # If the input vertical step is bigger than the maximum (the vertical FoV), then the maximum is assumed
        stepv = FoVv
    if stepv < 3:                                       # If the input vertical step is less than the minimum achievable by the system (), then the minimum is assumed
        stepv = 3

    if (2*FoVh % steph) != 0:
        FoVh = (2*FoVh - (2*FoVh % steph))/2
    if (2*FoVv % stepv) != 0:
        FoVv = (2*FoVv - (2*FoVv % stepv))/2

    FoVh = float(FoVh)/10000
    FoVv = float(FoVv)/10000
    steph = float(steph)/10000
    stepv = float(stepv)/10000

    N = ((2*FoVh/steph)+1)*((2*FoVv/stepv)+1)          # Calculation of the total number of points in the point cloud
    #N = 63	                                            # Total number of points in the point cloud for the artificial photos
    #N = 10

    # print(start_not_stop)                               # ROS - É NESTE SÍTIO QUE, EM VEZ DE PRINTS, DEVES MANDAR AQUELES VALORES PARA O EXTERIOR
    # print(FoVh)                                         #     - start_not_stop e N SAO INTEIROS; - FoVh, FoVv, steph E stepv SÃO FLOATS
    # print(FoVv)
    # print(steph)
    # print(stepv)
    # print(N)

    param = Float32MultiArray()
    param.data = [FoVh,FoVv,steph,stepv]
    pub1.publish(param)
    #pub2.publish(N)
	
    # PARCEIRO, LINHAS ABAIXO:
    #a.scatter(tmpxList, tmpyList, c = '#000000', cmap = 'viridis_r', linewidth = 10)
	# Penso que aqui não devas fazer scatter, mas apenas declarar a figura
    # Assim: 
    #f = Figure(figsize=(5.28,3.54))                           # Pointcloud figure creation
    #a = f.add_subplot(111) # 111, projection='3d'
    # talvez seja por causa desta linha que aparece uma segunda point cloud

    global xList, yList, zList 

    del xList[:]
    del yList[:]
    del zList[:]
    

    # xList.clear()									    ###ESTAS LINHAS VÃO FAZER MAIS SENTIDO DEPOIS DE VEREM A FUNÇÃO ANIMATE. MAS ISTO ESSENCIALMENTE
    # yList.clear()										###É A DECLARAÇÃO DE ARRAYS GLOBAIS PARA GUARDAREM OS PONTOS QUE VÃO RECEBENDO DA PROCESSING UNIT
    # zList.clear()										#### OS ARRAYS SÃO PREENCHIDOS NA FUNÇÃO ANIMATE

def change_state_stop():

    start_not_stop = 0
    # Activate entries when the system is not working
    opFoVh.config(state='normal')
    opFoVv.config(state='normal')
    opsteph.config(state='normal')
    opstepv.config(state='normal')

    # print(start_not_stop)                               # ROS - AQUI TAMBEM DEVES PUBLICAR O start_not_stop NO NÓ DE ROS (APENAS ESTE SINAL, NESTE CASO)

    pub3.publish(start_not_stop)




def animate(i):                                         # Pointcloud update function

    global xList, yList, zList, N
 
    xList.append(i.x)
    yList.append(i.y)
    zList.append(i.z)

    #rospy.loginfo(xList)
    #rospy.loginfo(yList)
    #rospy.loginfo(zList)

    
    rospy.loginfo(len(xList))

    if(len(xList) == N):    
        
        #a.clear()
        a = f.add_subplot(111, projection='3d')
        a.scatter(xList, yList,zList, cmap = 'viridis_r', linewidth = 1)
        f.canvas.draw_idle()
               
        del xList[:]
        del yList[:]
        del zList[:]
        		
        rospy.loginfo('Point Cloud') 

def animate_left(i):
    
    global xList_L, yList_L, N

    xList_L.append(i.x)
    yList_L.append(i.y)

    #rospy.loginfo(xList_L)
    #rospy.loginfo(yList_L)

    if(len(xList_L) == N):

        a_left = f_left.add_subplot(111)
        a_left.scatter(xList_L,yList_L, linewidth = 1)
        f_left.canvas_left.draw_idle()

        del xList_L[:]
        del yList_L[:]

def animate_right(i):
    
    global xList_R, yList_R, N

    xList_R.append(i.x)
    yList_R.append(i.y)

    #rospy.loginfo(xList_L)
    #rospy.loginfo(yList_L)

    if(len(xList_R) == N):

        a_right = f_right.add_subplot(111)
        a_right.scatter(xList_R,yList_R, linewidth = 1)
        f_right.canvas_right.draw_idle()

        del xList_R[:]
        del yList_R[:]

                  
       

def take_photo():

    pub_trigger.publish(1)
    


class OrisDashboard(tk.Tk):

    def __init__(self, *args, **kwargs):                # args for variables, kwargs for dictionaries

        tk.Tk.__init__(self, *args, **kwargs)           # initialize tkinter
        tk.Tk.wm_title(self, "LiDART - Dashboard")

        container = tk.Frame(self)                      # contains everything in the tkinter app (all the frames)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}                                # defines a dictionary (empty) for all the pages
        frame = RunPage(container, self)
        self.frames[RunPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        #frame = Page2(container, self)
        #self.frames[Page2] = frame
        #frame.grid(row=0, column=0, sticky="nsew")
        #self.show_frame(RunPage)

    def show_frame(self, cont):                         # raises the frame cont to the front
        frame = self.frames[cont]
        frame.tkraise()

    def quit_function(self):                            # function to exit the GUI
        pub4.publish(1)
        exit()

class RunPage(tk.Frame):    # Main page of the GUI (system's dashboard)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        path = os.path.dirname(os.path.abspath(__file__))   # get the current file's directory path

        # GUI title
        title = Label(self, text = "LiDART - DASHBOARD", font=('LARGE_FONT',18)).place(x = 800, y = 12)

        # Point cloud
        point_label = tk.Label(self, text = "Point Cloud View", font = ('LARGE_FONT',14)).place(x = 50, y = 55)
        canvas = FigureCanvasTkAgg(f, self)     # bring the Pointcloud canvas forward
        canvas.draw()
        canvas.get_tk_widget().place(x = 50, y = 90)

        # left
        left_label = tk.Label(self, text = "Left Camera View", font = ('LARGE_FONT',14)).place(x = 1200, y = 55)
        canvas_left = FigureCanvasTkAgg(f_left,self)
        canvas_left.draw()
        canvas_left.get_tk_widget().place(x = 1200,y = 90)

        # right
        right_label = tk.Label(self, text = "Right Camera View", font = ('LARGE_FONT',14)).place(x = 1200, y = 410)
        canvas_right = FigureCanvasTkAgg(f_right,self)
        canvas_right.draw()
        canvas_right.get_tk_widget().place(x = 1200,y = 440)
     
        global opFoVh, opFoVv, opsteph, opstepv

        # Laser Pattern choice (Input Parameters)
        mirrortext = Label(self, text = "Mirror pattern settings:", font=('LARGE_FONT',15)).place(x = 50, y = 750) # position of the label

        # Horizontal FoV
        lFovh = Label(self, text = "Horizontal FoV: ", font=('LARGE_FONT',12)).place(x = 50, y = 810)
        opFoVh = Entry(self, font=('LARGE_FONT',15),state='normal')
        opFoVh.place(x = 200, y = 810)

        # Vertical FoV
        lFovv = Label(self, text = "Vertical FoV: ", font=('LARGE_FONT',12)).place(x = 50, y = 850)
        opFoVv = Entry(self, font=('LARGE_FONT',15),state='normal')
        opFoVv.place(x = 200, y = 850)

        # Horizontal step
        lsteph = Label(self, text = "Horizontal step: ", font=('LARGE_FONT',12)).place(x = 550, y = 810)
        opsteph = Entry(self, font=('LARGE_FONT',15),state='normal')
        opsteph.place(x = 700, y = 810)

        # Vertical step
        lstepv = Label(self, text = "Vertical step: ", font=('LARGE_FONT',12)).place(x = 550, y = 850)
        opstepv = Entry(self, font=('LARGE_FONT',15),state='normal')
        opstepv.place(x = 700, y = 850)

        # Run button
        button_run = tk.Button(self,text="RUN",command= lambda *args: change_state_start(), height = 4, width = 14, font=('LARGE_FONT',15))
        button_run.place(x = 1000, y = 800)
        # Quit button
        button_quit = tk.Button(self,text="QUIT",command=lambda: controller.quit_function(), height = 4, width = 14, font=('LARGE_FONT',15))
        button_quit.place(x = 1250, y = 800)
        #Take Photo button
        btn_photo = tk.Button(self,text = "Take Photo", command =lambda *args: take_photo() ,height = 4, width = 14, font=('LARGE_FONT',15))
        btn_photo.place(x = 1500, y = 800)



# Execution of the gui
def dashboard():
    global pub1
    global pub2
    global pub3
    global pub4
    global pub_trigger

    rospy.init_node('dashboard', anonymous=True)
    gui = OrisDashboard()
    gui.geometry("1920x1280")
    #ani = animation.FuncAnimation(f, animate, interval=1000)    # Update period in ms - corresponds to the minimum refresh frequency of the point cloud
    rospy.Subscriber("Coordinates", Point, animate)     # tópico Spot_Coordinates
    rospy.Subscriber("Coordinates_left",Point,animate_left)
    rospy.Subscriber("Coordinates_right",Point,animate_right)
    #rospy.Subscriber("Coordinates", PoseArray, mindistance)
    pub1 = rospy.Publisher('Mirror_Pattern', Float32MultiArray, queue_size=10)
    #pub2 = rospy.Publisher('numberOfPoints', Int8, queue_size=10)
    pub3 = rospy.Publisher('Stop', Int8, queue_size=10)
    pub4 = rospy.Publisher('Quit', Int8, queue_size=10)
    pub_trigger = rospy.Publisher('take_photo', Int8 ,queue_size = 10)

	
            
    gui.mainloop()
    rospy.spin()

if __name__ == '__main__':
    try:
        dashboard()
    except rospy.ROSInterruptException:
        pass
