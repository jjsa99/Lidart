import matplotlib.pyplot as plt
from numpy import arange

FOVhor = float(input("FovH: "))
FOVvert = float(input("FovV: "))
stephor = float(input("stephor: "))
stepvert = float(input("stepvert: "))
negFOVV = -FOVvert
print("neg vert: ",negFOVV)
negFOVH = -FOVhor
print("neg hor: ",negFOVH)
negstepV = -stepvert
ax = plt.subplot(1,1,1)
Xlist = []
Ylist = []
init = 1 # init statement, in order for the system to start
yy = -1

# arrange alone doesn't accept float

for x in arange(negFOVH,FOVvert+1.0,stephor):
    print(x)
    if(yy <=0):
        for y in arange(negFOVV,(FOVvert+1.0),stepvert):
            Xlist.append(x)
            Ylist.append(y)
            yy = y
            print("x:", x)
            print("y:", y)
            print("yy: ",yy)
    elif yy >0:
        for y in arange(FOVvert,(negFOVV-1.0),negstepV):
            Xlist.append(x)
            Ylist.append(y)
            yy = y
            print("x:", x)
            print("y:", y)
            print("yy: ",yy)

plt.scatter(Xlist[:],Ylist[:])


plt.grid()
plt.show()
