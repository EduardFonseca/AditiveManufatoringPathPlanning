#make a zig-zag path inside a polygon
#the path is a list of points
#the points are a list of x,y,z coordinates
#the z coordinate is the height of the nozzle above the bed


#FIXME: Problem wgen there is more then 2 dots in the same x coordinate
#FIXME: Problem when the polygon has a side underneath the zigzag
#TODO: Generate a offset in the segments to make the zig-zag path
#TODO: organize the variables in objects to make it more readable
#TODO: organize in functions

import numpy as np
import math
import matplotlib.pyplot as plt

#==============================================================================
# #defining the polygons
#==============================================================================

#defining the polygon (circle)
# r = 10
# n = 100
# theta = np.linspace(0,2*np.pi,n)
# poly = np.array([r*np.cos(theta),r*np.sin(theta)]).T

# #put a new small circle inside the circle (FIXME1)
# r = 5
# poly2 = np.array([r*np.cos(theta),r*np.sin(theta)]).T
# poly = np.concatenate((poly,poly2))

#defining a non comvex polygon (FIXME2)
poly = np.array([[0,0],[0,10],[10,10],[10,0],[5,5]])
#rotate the polygon
theta = np.pi/2
R = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
poly = np.dot(poly,R)

#==============================================================================
# printer settings
#==============================================================================

#defining the nozzle size and the distance between the zig-zags lines
nozzle = 0.4
line_distance = 0.9*nozzle

#finding the bouting box of the polygon
minx = np.min(poly[:,0])
maxx = np.max(poly[:,0])
miny = np.min(poly[:,1])
maxy = np.max(poly[:,1])

bb = np.array([[minx,miny],[minx,maxy],[maxx,maxy],[maxx,miny]])

#Split bb vertically with lines (number of lines = bb.width/line_distance)
#and find the intersection points with the polygon
#the intersection points are the start and end points of the zig-zag lines

#find the number of lines
n_lines = int((maxx-minx)/line_distance)

#find the x coordinates of the lines
x_lines = np.linspace(minx,maxx,n_lines)

#find the intersection points
points = []

#TODO: compleately underestand the loop
for i in range(len(x_lines)):
    #find the intersection points with the polygon
    for j in range(len(poly)):
        #find the intersection points with the bounding box
        if j == len(poly)-1:
            if (poly[j,0] < x_lines[i] < poly[0,0]) or (poly[j,0] > x_lines[i] > poly[0,0]):
                if poly[j,1] == poly[0,1]:
                    points.append([x_lines[i],poly[j,1]])
                else:
                    m = (poly[0,1]-poly[j,1])/(poly[0,0]-poly[j,0])
                    b = poly[j,1]-m*poly[j,0]
                    y = m*x_lines[i]+b
                    points.append([x_lines[i],y])
        else:
            if (poly[j,0] < x_lines[i] < poly[j+1,0]) or (poly[j,0] > x_lines[i] > poly[j+1,0]):
                if poly[j,1] == poly[j+1,1]:
                    points.append([x_lines[i],poly[j,1]])
                else:
                    m = (poly[j+1,1]-poly[j,1])/(poly[j+1,0]-poly[j,0])
                    b = poly[j,1]-m*poly[j,0]
                    y = m*x_lines[i]+b
                    points.append([x_lines[i],y])

#construct segmentes between the points with the same x coordinate
#FIXME: a point cant be in more then 2 segments
segments = []
for i in range(len(points)):
    if i == len(points)-1:
        if points[i][0] == points[0][0]:
            segments.append([points[i],points[0]])
    else:
        if points[i][0] == points[i+1][0]:
            segments.append([points[i],points[i+1]])


#join the closest ends of the segments to make a zig-zag path
path = []
for i in range(len(segments)):
    if i!=len(segments)-1:
        if i==0:
            end_point = segments[i][1]
        else:
            start_point = path[-1][1]
            if start_point == segments[i][0]:
                end_point = segments[i][1]
            else:
                end_point = segments[i][0]
        candidate1 = segments[i+1][0]
        candidate2 = segments[i+1][1]
        distance1 = np.sqrt((end_point[0]-candidate1[0])**2+(end_point[1]-candidate1[1])**2)
        distance2 = np.sqrt((end_point[0]-candidate2[0])**2+(end_point[1]-candidate2[1])**2)
        if distance1 < distance2:
            path.append(segments[i])
            path.append([end_point,candidate1])
        else:
            path.append(segments[i])
            path.append([end_point,candidate2])
    else:
        path.append(segments[i])

plt.figure()
#plot poly and points
# plt.plot(poly[:,0],poly[:,1])
# plt.plot([p[0] for p in points],[p[1] for p in points],'o')
#plot path
for segment in segments:
    plt.plot([segment[0][0],segment[1][0]],[segment[0][1],segment[1][1]])

plt.show()


