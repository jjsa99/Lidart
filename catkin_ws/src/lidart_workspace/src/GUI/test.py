#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


import rospy
from std_msgs.msg import Int8
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Pose
import time
import os

def OrisDashboard():
    
    root = tk.Tk()    
    path = os.path.dirname(os.path.abspath(__file__))   # get the current file's directory path

    #title = tk.Label(self, text = "LiDART - DASHBOARD", font=('LARGE_FONT',18))
    #title.place(x = 450, y = 12)


    img = Image.open(path + "/normal_photo.bmp")
    img = img.resize((567,354))
    img_render = ImageTk.PhotoImage(img)
    # img_attrib = tk.Label(self,image = img_render)
    # img_attrib.place(x = 6, y = 54)

    panel = Label(root,image = img_render)
    panel.pack(side = "bottom", fill = "both", expand = "yes")


    #Start the program

    root.mainloop()


# Execution of the gui
def dashboard():

    rospy.init_node('dashboard', anonymous=True)
    OrisDashboard()
	
    rospy.spin()

if __name__ == '__main__':
    try:
        dashboard()
    except rospy.ROSInterruptException:
        pass
