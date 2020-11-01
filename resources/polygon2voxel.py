import os
import glob
import tqdm
import argparse
import numpy as np
import meshio
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
import pdb

def read_off(path):
    mesh = meshio.read(path,file_format="off")
    vertices = mesh.points
    faces = np.array(mesh.cells[0].data)
    return vertices,faces

def check(V,VS):
    V1 = (V[:,0]<1)|(V[:,0]>VS[0])
    V2 = (V[:,1]<1)|(V[:,1]>VS[1])
    V3 = (V[:,2]<1)|(V[:,2]>VS[2])
    return ~(V1|V2|V3)

def checkABC(VA,VB,VC,VS):
    checkA = check(VA,VS)
    checkB = check(VB,VS)
    checkC = check(VC,VS)
    return checkA,checkB,checkC

def intf(V):
    iV0 = np.round(V[:,0]).astype(int)
    iV1 = np.round(V[:,1]).astype(int)
    iV2 = np.round(V[:,2]).astype(int)
    return iV0-1,iV1-1,iV2-1

def polygon2voxel(FV,VolumeSize,mode='auto',Yxz=True):
    if len(VolumeSize)==1:
        VolumeSize = [VolumeSize,VolumeSize,VolumeSize]
    assert len(VolumeSize)==3, "VolumeSize must be a array of 3 elements"
    
    Vertices = FV['vertices']
    Faces = FV['faces']
    VolumeSize = np.array(VolumeSize)
    sizev = Vertices.shape
    sizef = Faces.shape
    assert (sizev[1]==3)|(len(sizev)==2),"The vertice list is not a mx3 array"
    assert (sizef[1]==3)|(len(sizef)==2),"The face list is not a mx3 array"
    assert np.max(Faces[:])<=Vertices.shape[0],"The face list contains an undefined vertex index"
    assert np.min(Faces[:])>=0,"The face list contains an vertex index smaller than 0"
    assert mode != "clamp","The mode clamp is not available"
    if Yxz:
        Vertices = Vertices[:,[1,0,2]]
    if mode.lower() == 'auto':
        Vertices = Vertices - np.min(Vertices,axis=0)
        scaling = np.min((VolumeSize-1)/np.max(Vertices,axis=0))
        Vertices = Vertices*scaling+1
        Wrap = 0
    elif mode.lower() == 'center':
        Vertices = Vertices + VolumeSize/2
        Wrap = 0
    elif mode.lower() == 'warp':
        Wrap = 1
    elif mode.lower() == 'clamp':
        Wrap = 2
    else:
        Wrap = 0
    Volume = np.zeros(VolumeSize)
    VeA = Vertices[Faces[:,0],:]
    VeB = Vertices[Faces[:,1],:]
    VeC = Vertices[Faces[:,2],:]
    VS = VolumeSize
    
    while not np.all(VeA==0):
        VolumeSize = Volume.shape
        if Wrap == 0:
            checkA,checkB,checkC = checkABC(VeA,VeB,VeC,VS)
            VA = VeA[checkA,:]
            VB = VeB[checkB,:]
            VC = VeC[checkC,:]
        elif Wrap == 1:
            VA = (VeA-1)*VS + 1
            VB = (VeB-1)*VS + 1
            VC = (VeC-1)*VS + 1
        else:
            pass
        iVA0,iVA1,iVA2 = intf(VA)
        iVB0,iVB1,iVB2 = intf(VB)
        iVC0,iVC1,iVC2 = intf(VC)
        Volume[iVA0,iVA1,iVA2] = True
        Volume[iVB0,iVB1,iVB2] = True
        Volume[iVC0,iVC1,iVC2] = True

        VS = Volume.shape
        if Wrap == 0:
            check1=(VeA[:,0]<1)&(VeB[:,0]<1)&(VeC[:,0]<1)
            check2=(VeA[:,1]<1)&(VeB[:,1]<1)&(VeC[:,1]<1)
            check3=(VeA[:,2]<1)&(VeB[:,2]<1)&(VeC[:,2]<1)
            check4=(VeA[:,0]>VS[0])&(VeB[:,0]>VS[0])&(VeC[:,0]>VS[0])
            check5=(VeA[:,1]>VS[1])&(VeB[:,1]>VS[1])&(VeC[:,1]>VS[1])
            check6=(VeA[:,2]>VS[2])&(VeB[:,2]>VS[2])&(VeC[:,2]>VS[2])
            outside=check1|check2|check3|check4|check5|check6
            VeA = VeA[~outside,:]
            VeB = VeB[~outside,:]
            VeC = VeC[~outside,:]

        VeAnew = np.zeros((0,3))
        VeBnew = np.zeros((0,3))
        VeCnew = np.zeros((0,3))

        if not np.all(VeA==0):
            dist1=(VeA[:,0]-VeB[:,0])**2+(VeA[:,1]-VeB[:,1])**2+(VeA[:,2]-VeB[:,2])**2
            dist2=(VeC[:,0]-VeB[:,0])**2+(VeC[:,1]-VeB[:,1])**2+(VeC[:,2]-VeB[:,2])**2
            dist3=(VeC[:,0]-VeA[:,0])**2+(VeC[:,1]-VeA[:,1])**2+(VeC[:,2]-VeA[:,2])**2
            dist = np.vstack((dist1,dist2,dist3))
            maxdist = np.max(dist,axis=0)
            maxindex = np.argmax(dist,axis=0)
            split = maxdist > 0.5
            m1 = (maxindex==0)&split
            m2 = (maxindex==1)&split
            m3 = (maxindex==2)&split

            if m1.any():
                VA = VeA[m1,:]
                VB = VeB[m1,:]
                VC = VeC[m1,:]
                VN = (VA+VB)/2

                VeAnew = np.append(VeAnew,VN,axis=0)
                VeAnew = np.append(VeAnew,VA,axis=0)
                VeBnew = np.append(VeBnew,VB,axis=0)
                VeBnew = np.append(VeBnew,VN,axis=0)
                VeCnew = np.append(VeCnew,VC,axis=0)
                VeCnew = np.append(VeCnew,VC,axis=0)
            if m2.any():
                VA = VeA[m2,:]
                VB = VeB[m2,:]
                VC = VeC[m2,:]
                VN = (VC+VB)/2

                VeAnew = np.append(VeAnew,VA,axis=0)
                VeAnew = np.append(VeAnew,VA,axis=0)
                VeBnew = np.append(VeBnew,VN,axis=0)
                VeBnew = np.append(VeBnew,VB,axis=0)
                VeCnew = np.append(VeCnew,VC,axis=0)
                VeCnew = np.append(VeCnew,VN,axis=0)
            if m3.any():
                VA = VeA[m3,:]
                VB = VeB[m3,:]
                VC = VeC[m3,:]
                VN = (VA+VC)/2

                VeAnew = np.append(VeAnew,VN,axis=0)
                VeAnew = np.append(VeAnew,VA,axis=0)
                VeBnew = np.append(VeBnew,VB,axis=0)
                VeBnew = np.append(VeBnew,VB,axis=0)
                VeCnew = np.append(VeCnew,VC,axis=0)
                VeCnew = np.append(VeCnew,VN,axis=0)

        VeA = VeAnew
        VeB = VeBnew
        VeC = VeCnew
    
    return Volume

def poly2voxN(file,res=32,num_rotations=24):
    data = np.zeros((1,num_rotations,res,res,res))
    vertices, faces = read_off(file)
    vertices = vertices - np.mean(vertices,axis=0)
    FV = {}; FV['faces'] = faces
    # j loop
    for j in range(num_rotations):
        th = 2*np.pi*j/num_rotations
        tm1 = vertices[:,0]*np.cos(th)-vertices[:,1]*np.sin(th)
        tm2 = vertices[:,0]*np.sin(th)+vertices[:,1]*np.cos(th)
        tm3 = vertices[:,2]
        vs = np.vstack((tm1,tm2,tm3))
        FV['vertices'] = vs.T
        Volume = polygon2voxel(FV,[res,res,res])
        data[0,j,:,:,:] = Volume.copy()
    return data



if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--res',type=int,default=16)
    p.add_argument('--num_rotations',type=int,default=24)
    p.add_argument('--offpath',type=str,default='/home/yui/Documents/data/ModelNet10/chair/train/chair_0001.off')
    args = p.parse_args()

    data = poly2voxN(args.offpath,res=args.res,num_rotations=args.num_rotations)

    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111,projection="3d")
    ax.voxels(data[0,10,:,:,:],facecolors='aqua',edgecolor="r")
    ax.view_init(45,40)
    plt.show()

    pdb.set_trace()




















