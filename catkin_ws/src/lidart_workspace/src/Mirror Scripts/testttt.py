import numpy 
import math

FOVhor = 4
FOVvert = 5
stephor = 1.5
stepvert = 1  
  
nPointsHorizontal = math.floor(FOVhor/stephor)+1
nPointsVertical = math.floor(FOVvert/stepvert)+1

mirrorPositions = list()

for hor in range(0, nPointsHorizontal-1):
	tmp1 = hor*stephor-FOVhor/2
	for ver in range(0, nPointsVertical-1):
		tmp2 = ver*stepvert-FOVvert/2
		mirrorPositions[hor+ver] = [tmp1, tmp2]
		mirrorPositions

