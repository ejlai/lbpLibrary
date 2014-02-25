#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Hlavní soubor pySlam
---------------------

"""

# import funkcí
import sys
import os.path
import numpy as np
import scipy

def initPoints(N, c):
	surface = 4*np.pi
	pointsurface = surface/N
	r = np.sqrt(pointsurface/np.pi)
	distance = 2*r;
	points = np.zeros([N,4], dtype = np.double)
	points[0,:] = [0,0,1,0]
	
	for i in range(6) :
		helpPoint =  points[0,0:3] + [np.cos((i)*np.pi/3)*distance,np.sin((i)*np.pi/3)*distance,0]
		helpPoint = helpPoint/np.linalg.norm(helpPoint) 
		helpPoint2 = helpPoint - points[0,0:3]      
		helpPoint2 = helpPoint2/np.linalg.norm(helpPoint2)
		for j in range(10):
			helpPoint =  points[0,0:3] + helpPoint2*distance
			helpPoint = helpPoint/np.linalg.norm(helpPoint)  
			helpPoint2 = helpPoint - points[0,0:3]
			helpPoint2 = helpPoint2/np.linalg.norm(helpPoint2)        
		points[i+1,0:3] = points[0,0:3] + helpPoint2*distance
		points[i+1,0:3] = points[i+1,0:3]/np.linalg.norm(points[i+1,0:3])
		points[i+1,3] = helpPoint[2]
		
	ind = 7
	i = 1
	while (ind < N):
		for m in range(6):
			if(ind >= N):
				break

			if i >= N: 
				ind = N+1
				break
				
			helpPoint =  points[i,0:3] + [np.cos((m)*np.pi/3)*distance,np.sin((m)*np.pi/3)*distance,-points[i,3]]
			helpPoint = helpPoint/np.linalg.norm(helpPoint)
			helpPoint2 = helpPoint - points[i,0:3]      
			helpPoint2 = helpPoint2/np.linalg.norm(helpPoint2)
			for k in range(20):
				helpPoint =  points[i,0:3] + helpPoint2*distance
				helpPoint = helpPoint/np.linalg.norm(helpPoint) 
				helpPoint2 = helpPoint - points[i,0:3]
				helpPoint2 = helpPoint2/np.linalg.norm(helpPoint2)        
			ok = 1;
			helpPoint = points[i,0:3] + helpPoint2*distance
			helpPoint = helpPoint/np.linalg.norm(helpPoint)          
			for k in range(N):
				if(k == i):
					continue;
				npnorm = np.linalg.norm(helpPoint - points[k,0:3])
				if(npnorm < c*distance):
					ok = 0 
						
			if(ok == 1):        
				points[ind,0:3] = helpPoint
				ind = ind + 1
		i = i+1;
		
	points2 = points[:,0:3]
	points = points2		
	return points
	
def spherePoints(N, sphereSize, iterations, c, initType):
	if initType == 1:
		points = initPoints(N,c)
	else:
		for i in range(N):
			points[i,:] = -1+ 2 * np.random.rand(1,3)
			normp = np.norm(points[i,:])
			points[i,:] = points[i,:]/normp

	for i in range(iterations):
		for j in range(N):
			mindist = 100000000
			minindex = 0
			actualdist = np.zeros([N,1], dtype = np.double);
			for k in range(N):
				if j == k:
					actualdist[k] = 1000
					continue
				actualdist[k] = np.linalg.norm(points[j,:] - points[k,:]);         
			minindex = np.argmin(actualdist);
			actualdist[minindex] = 1000000;
			for l in range(4):
				dindex = np.argmin(actualdist);    
				actualdist[dindex] = 1000000;         
			maxmindist = np.min(actualdist);
			minvector = points[minindex,:] - points[j,:];
			points[j,:] = points[j,:] - c*(1 - (mindist/maxmindist))*minvector;
			normp = np.linalg.norm(points[j,:]);
			points[j,:] = points[j,:]/normp;        
	points = points*sphereSize;
	return points
	
def maskGenerator(N, width, height, sphereRadius, iterations, c, initType):
	points = {} 
	offset = sphereRadius + 1;
	p = spherePoints(N, sphereRadius, iterations, c, initType);
	p = p+offset
	mask = np.zeros([p.shape[0]*8,1], dtype = np.double);
 	maskCoef = np.zeros([p.shape[0]*8,1], dtype = np.double);
	for i in range(p.shape[0]):
		temp = p[i,:];
		temp1 = np.round(temp);    
		x = [temp[0]-0.5, temp[0]+0.5];
		y = [temp[1]-0.5, temp[1]+0.5];
		z = [temp[2]-0.5, temp[2]+0.5];
		m = 0;
		for j in range(2):
			for k in range(2):
				for l in range(2):
					mask[(i-1)*8 + m] = np.floor(x[j]) + np.floor(y[k])*width + np.floor(z[l])*width*height;                
					maskCoef[(i-1)*8 + m] =  np.abs(x[j]-temp1[0])*np.abs(y[k]-temp1[1])*np.abs(z[l]-temp1[2]);
					m = m + 1;
	points['center'] = np.floor(offset) + np.floor(offset)*width + np.floor(offset)*width*height; 
	points['mask'] = mask
	points['maskCoef'] = maskCoef
	return points
	
def lbp3DLoadLibrary() :
    """Function loads LBP library

			 RealtimeLbp.dll/libRealtimeLbp.so (win/lin)
    """
    lbplib = ctypes.cdll.LoadLibrary("${DYNLIB}")
    return lbplib	
	
def lbp3d(lbplib, npIM, N, mask, radius):
		s = npIM.shape[0]
		r = npIM.shape[1]
		c = npIM.shape[2]    

		img = (ctypes.c_long * (r*c*s))()
		res = (ctypes.c_long * np.pow(2,N))()
		maskPoints = (ctypes.c_long * N * 8)()
		maskCoef = (ctypes.c_double * N * 8)()    

		for i in range(N*8):
			maskPoints[i] = mask['mask'][i]
			maskCoef[i] = mask['maskCoef'][i]

		for i in range(s) :
			for j in range(r) :
				for k in range(c) :
					img[(r*c*i) + (c*j) + k] = npIM[i,j,k]
		lbplib.lpb3d(r,c,s, ctypes.byref(maskPoints), ctypes.byref(maskCoef), N, mask['center'], radius, ctypes.byref(img), ctypes.byref(res))
		res2 = zeros([1, np.pow(2,N)], dtype = np.int32)
		for i in range(np.pow(2,N))
			res2[i] = res[i]
    return res2


	








