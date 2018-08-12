#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 01:32:48 2018

@author: anand
"""
import homework4_data as data
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# load and plot mys1
mys1_data = data.mystery1
x0 = []
y0 = []

x1 = []
y1 = []
for item in mys1_data:
	if item[1] == False:
		x0.append(item[0][0])
		y0.append(item[0][1])
	else:
		x1.append(item[0][0])
		y1.append(item[0][1]) 
# plotting
plt.scatter(x0, y0, color='red')
plt.hold
plt.scatter(x1, y1, color='blue')
plt.show()

# load and plot mys2
mys2_data = data.mystery2
x0 = []
y0 = []
z0 = []

x1 = []
y1 = []
z1 = []

for item in mys2_data:
	if item[1] == False:
		x0.append(item[0][0])
		y0.append(item[0][1])
		z0.append(item[0][2])
	else:
		x1.append(item[0][0])
		y1.append(item[0][1])
		z1.append(item[0][2])
# plotitng
plt.scatter(x0, y0, z0, color='red')
plt.hold
plt.scatter(x1, y1, z1, color='blue')
plt.show()