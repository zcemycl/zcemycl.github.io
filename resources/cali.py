import matplotlib.pyplot as plt
import numpy as np
from numpy import matmul as mm
from numpy.linalg import inv as inv
import pdb
import scipy

# Rigid body transformation
print(np.sin(np.pi))
phi = np.pi/3
Pr = np.array([[np.cos(phi),-np.sin(phi),0,2],
               [np.sin(phi),np.cos(phi),0,1],
               [0,0,1,0]])
print("rigid body transform: ",Pr)

# projection matrix
Pp = np.array([[.5,0,0],[0,.5,0],[0,0,1]])
print("perspective project: ",Pp)

# ccd imaging
Pc = np.array([[1.1,0,5],[0,.2,4],[0,0,1]])
print("CCD imaging: ",Pc)

# result
K = mm(Pc,Pp)
Pps = mm(K,Pr)
print("calibration matrix: ")
print(K)
print("projection matrix: ")
print(Pps)

# QR decomposition to rotation
M = Pps[:3,:3]
print("M")
print(M)
print("QR decomposition#")
q,r = np.linalg.qr(np.linalg.inv(M))
q,r = inv(q),inv(r)
#q,r = np.linalg.qr(M)
print('q is the rotation')
print(q)
print('r is the calibration')
print(r)

# recovery of translation
print(Pps[:,3:])
print(mm(inv(r),Pps[:,3:]))

pdb.set_trace()
