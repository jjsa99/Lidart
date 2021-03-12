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
#from tkFont import Font



LARGE_FONT=("Verdana",14)
style.use("dark_background")

start_not_stop = 0
xList = []					#Arrays onde vão ser guardados os pontos que vêm do Processing Unit
yList = []
zList = []

tmpxList = []
tmpyList = []

N = 0

# Point cloud plot
f = plt.figure(figsize=(5.28,3.54))
a = plt.subplot()
plt.ion()

# left plot
f_left = plt.figure(figsize = (5,5))
a_left = f_left.add_subplot(111)

# right plot
f_right = plt.figure(figsize = (5,5))
a_right = f_right.add_subplot(111)




def change_state_start():

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
    
    del tmpxList[:]
    del tmpyList[:]

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
    global tmpxList, tmpyList
 
    xList.append(i.x)
    yList.append(i.y)
    zList.append(i.z)
    
    tmpxList.append(i.x)
    tmpyList.append(i.y)

    rospy.loginfo(xList)
    rospy.loginfo(yList)
    rospy.loginfo(zList)

    
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
         
       
        
        #Unused lines of code
        #plt.draw_if_interactive()
        #plt.draw()
        #a.axis('off')
        #a.set(xlim=(0, 1), ylim=(-0.4, 0.4))
        #a.axis('image')
        #a.grid(False)
        #a.scatter(xList, yList, zList, c = zList, cmap = 'viridis_r', linewidth = 1)    # Point cloud plot in the GUI
        #rospy.loginfo(xList)
        #rospy.loginfo(yList)
        #rospy.loginfo(zList)
        #plt.clf()
        #a.clear()

def take_photo():

    pub_trigger.publish(1)
    path_left = '/home/lidart/init_photos/left/left_init.png'
    path_right = '/home/lidart/init_photos/right/right_init.png'

    while(os.path.isfile(path_left) == 0) and (os.path.isfile(path_right) == 0 ):
        rospy.loginfo("1")
        rospy.sleep(1)

    rospy.sleep(2)
    rospy.loginfo("2")
    # left 
    img_left = plt.imread(path_left)
    a_left.imshow(img_left)

    # right
    img_right = plt.imread(path_right)
    a_right.imshow(img_right)
    


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

        # #Foto of the physical scenario, captured by the left camera
        # load_photo = PIL.Image.open(path+"/normal_photo.bmp")                         # ESTA IMAGEM TAMBÉM DEVE SER LIDA DO NÓ ROS
        # new_photo = load_photo.resize((567, 354))
        # render_photo = ImageTk.PhotoImage(new_photo)
        # photo = Label(self, image = render_photo)
        # photo.image = render_photo
        # photo.place(x = 6, y = 54)
        # photo_label = Label(self, text = "[photo of the pyshical scene captured by the left camera]", font=('LARGE_FONT',10))
        # photo_label.place(x = 102, y = 417)


        # Point cloud
        canvas = FigureCanvasTkAgg(f, self)     # bring the Pointcloud canvas forward
        canvas.draw()
        canvas.get_tk_widget().place(x = 1200, y = 100)
        #canvas_label = Label(self, text = "[pointcloud of the scene produced by ORIS]", font=('LARGE_FONT',10)).place(x = 1200, y = 900)

        # left
        canvas_left = FigureCanvasTkAgg(f_left,self)
        canvas_left.draw()
        canvas_left.get_tk_widget().place(x = 50,y = 100)

        # right
        canvas_left = FigureCanvasTkAgg(f_right,self)
        canvas_left.draw()
        canvas_left.get_tk_widget().place(x = 600,y = 100)
     
        global opFoVh, opFoVv, opsteph, opstepv

        # Laser Pattern choice (Input Parameters)
        mirrortext = Label(self, text = "Mirror pattern settings:", font=('LARGE_FONT',15)).place(x = 50, y = 750) # position of the label

        # Horizontal FoV
        lFovh = Label(self, text = "Horizontal FoV: ", font=('LARGE_FONT',12)).place(x = 50, y = 810)
        opFoVh = Entry(self, font=('LARGE_FONT',15),state='normal').place(x = 200, y = 810)
        
        # Vertical FoV
        lFovv = Label(self, text = "Vertical FoV: ", font=('LARGE_FONT',12)).place(x = 50, y = 850)
        opFoVv = Entry(self, font=('LARGE_FONT',15),state='normal').place(x = 200, y = 850)

        # Horizontal step
        lsteph = Label(self, text = "Horizontal step: ", font=('LARGE_FONT',12)).place(x = 550, y = 810)
        opsteph = Entry(self, font=('LARGE_FONT',15),state='normal').place(x = 700, y = 810)

        # Vertical step
        lstepv = Label(self, text = "Vertical step: ", font=('LARGE_FONT',12)).place(x = 550, y = 850)
        opstepv = Entry(self, font=('LARGE_FONT',15),state='normal').place(x = 700, y = 850)

        # Run button
        button_run = tk.Button(self,text="RUN",command=lambda *args: change_state_start(), height = 4, width = 14, font=('LARGE_FONT',15)).place(x = 1000, y = 800)
        # Quit button
        button_quit = tk.Button(self,text="QUIT",command=lambda: controller.quit_function(), height = 4, width = 14, font=('LARGE_FONT',15)).place(x = 1250, y = 800)
        #Take Photo button
        btn_photo = tk.Button(self,text = "Take Photo", command =lambda *args: take_photo() ,height = 4, width = 14, font=('LARGE_FONT',15)).place(x = 1500, y = 800)


# class Page2(tk.Frame):  # Secondary page of the GUI (with specifications and instructions)

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         path = os.path.dirname(os.path.abspath(__file__)) # get the current file's directory pat

#         # GUI title
#         title = Label(self, text = "LiDART - DASHBOARD", font=('LARGE_FONT',18))
#         title.place(x = 450, y = 12)

#         # How to use the dashboard -title
#         instr_title = Label(self, text = "How to use the LiDART's dashboard:", font=('LARGE_FONT',12))
#         instr_title.place(x = 18, y = 47)

#         # Input parameters
#         input_title = Label(self, text = "1 - Define the input parameters:", font=('LARGE_FONT',11))
#         input_title.place(x = 24, y = 72)
#         input_intro = Label(self, text = "The input parameters the user can define are the horizontal and vertical field of view", font=('LARGE_FONT',9))
#         input_intro.place(x = 24, y = 97)
#         input_intro2 = Label(self, text = "considered by the system and the angular horizontal and vertical step used to scan", font=('LARGE_FONT',9))
#         input_intro2.place(x = 24, y = 115)
#         input_intro3 = Label(self, text = "the considered fiel of view. The way those parameters are considered, in practice,", font=('LARGE_FONT',9))
#         input_intro3.place(x = 24, y = 133)
#         input_intro4 = Label(self, text = "to configure the system are shown in the figure below.", font=('LARGE_FONT',9))
#         input_intro4.place(x = 24, y = 151)

#         # load_figure1 = PIL.Image.open(path+'/figure_1.jpg')
#         # new_figure1 = load_figure1.resize((414, 237))
#         # render_figure1 = ImageTk.PhotoImage(new_figure1)
#         # figure1 = Label(self, image = render_figure1)
#         # figure1.image = render_figure1
#         # figure1.place(x = 76, y = 176)

#         input_intro4 = Label(self, text = "The user must choose both the FOVs and both the steps, according to the next range", font=('LARGE_FONT',9))
#         input_intro4.place(x = 24, y = 423)
#         input_intro5 = Label(self, text = "and specifications:", font=('LARGE_FONT',9))
#         input_intro5.place(x = 24, y = 441)
#         input_FOV = Label(self, text = "a) 0.0003 degrees <= FOV <= 45 degrees;", font=('LARGE_FONT',9))
#         input_FOV.place(x = 48, y = 465)
#         input_step = Label(self, text = "b) 0.0003 degrees <= angular step <= FOV selected;", font=('LARGE_FONT',9))
#         input_step.place(x = 48, y = 483)
#         input_step_FOV = Label(self, text = "c) the FOV must be a complete multiple of the respective angular step.", font=('LARGE_FONT',9))
#         input_step_FOV.place(x = 48, y = 501)
#         input_adapt = Label(self, text = "If the specifications above are not fulfilled, the system will adjust the parameters in", font=('LARGE_FONT',9))
#         input_adapt.place(x = 24, y = 531)
#         input_adapt2 = Label(self, text = "order to fulfill them. This may lead to smaller FOVs and a behavior of the system that", font=('LARGE_FONT',9))
#         input_adapt2.place(x = 24, y = 549)
#         input_adapt3 = Label(self, text = "was not the expected by the user. That is why it is highly recommended to obey those", font=('LARGE_FONT',9))
#         input_adapt3.place(x = 24, y = 567)
#         input_adapt4 = Label(self, text = "specifications. Although the system will produceresults anyway, these may not be the", font=('LARGE_FONT',9))
#         input_adapt4.place(x = 24, y = 585)
#         input_adapt5 = Label(self, text = "needed and expected ones.", font=('LARGE_FONT',9))
#         input_adapt5.place(x = 24, y = 603)

#         # Control buttons
#         buttons_title = Label(self, text = "2 - Use the control buttons:", font=('LARGE_FONT',11))
#         buttons_title.place(x = 582, y = 72)
#         buttons_RUN = Label(self, text = "RUN: once the input parameters are all defined, the RUN button is used to make", font=('LARGE_FONT',9))
#         buttons_RUN.place(x = 588, y = 97)
#         buttons_RUN2 = Label(self, text = "the system to start producing results, accordingly to those parameters.", font=('LARGE_FONT',9))
#         buttons_RUN2.place(x = 588, y = 115)
#         buttons_STOP = Label(self, text = "STOP: when the system is running, this button can be used to pause/freeze the", font=('LARGE_FONT',9))
#         buttons_STOP.place(x = 588, y = 139)
#         buttons_STOP2 = Label(self, text = "system, so the user can change some input parameters and then re-start the", font=('LARGE_FONT',9))
#         buttons_STOP2.place(x = 588, y = 157)
#         buttons_STOP3 = Label(self, text = "system again with those new parameters, by pushing the RUN button again.", font=('LARGE_FONT',9))
#         buttons_STOP3.place(x = 588, y = 175)
#         buttons_QUIT = Label(self, text = "QUIT: this button is used to stop all the system and exit the dashboard window.", font=('LARGE_FONT',9))
#         buttons_QUIT.place(x = 588, y = 199)

#         # Output
#         output_title = Label(self, text = "System's output:", font=('LARGE_FONT',12))
#         output_title.place(x = 576, y = 229)
#         output_text = Label(self, text = "Besides the point cloud presented to the user in the dashboard, the system also", font=('LARGE_FONT',9))
#         output_text.place(x = 588, y = 254)
#         output_text2 = Label(self, text = "save the points' coordinates, on 3 .txt files, on the machine running the system.", font=('LARGE_FONT',9))
#         output_text2.place(x = 588, y = 272)
#         output_text3 = Label(self, text = "These files are named 'x_LiDART.txt', 'y_LiDART.txt' and 'z_LiDART.txt' and the", font=('LARGE_FONT',9))
#         output_text3.place(x = 588, y = 290)
#         output_text4 = Label(self, text = "coordinates are defined in the axel system of the figure below (the same system", font=('LARGE_FONT',9))
#         output_text4.place(x = 588, y = 308)
#         output_text5 = Label(self, text = "considered to construct the point cloud shown in the dashboard).", font=('LARGE_FONT',9))
#         output_text5.place(x = 588, y = 326)

#         # load_figure2 = PIL.Image.open(path+'/figure_2.jpg')
#         # new_figure2 = load_figure2.resize((259, 230))
#         # render_figure2 = ImageTk.PhotoImage(new_figure2)
#         # figure2 = Label(self, image = render_figure2)
#         # figure2.image = render_figure2
#         # figure2.place(x = 718, y = 351)

#         # Push button to go back to the main page
#         button_RunPage = tk.Button(self,text="Go back to the Dashboard",
#                             command=lambda: controller.show_frame(RunPage), height = 0, width = 57, font=('LARGE_FONT',10))
#         button_RunPage.place(x = 608, y = 590)


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
