import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import PIL.Image
from PIL import Image, ImageTk
from tkinter import *
import matplotlib.pyplot as plt

xList = [0,1,2,3,4,5,6,7,8,9]
yList = [10,11,12,13,14,15,16,17,18,19]
zList = [1,1,1,1,1,1,1,1,1,1]


# é o nosso widget principal
root = Tk()                

# queremos criar um widget  que seja um label que atue no nosso widget root
myLabel = Label(root, text = "Hello Word")

# vai mandar o myLabel para o ecra, mantem as coisas sempre no mesmo sitio
myLabel.pack()

# vai fazer loop até terminar o programa 
root.mainloop()
