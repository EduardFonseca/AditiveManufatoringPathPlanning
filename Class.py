#TODO: add comments
import numpy as np
import math
import matplotlib.pyplot as plt

#TODO: Generate a offset in the segments to make the zig-zag path
#TODO: organize the variables in objects to make it more readable
#TODO: organize in functions

class Slicer:
    def __init__(self, nozzle=0.4, line_distance=1):
        self.nozzle = nozzle
        self.line_distance = line_distance*self.nozzle
        self.poly = []

    def path2Gcode(self, path):
        #TODO: add calculation of extrusion per distance
        gcode = []
        for i in range(len(path)):
            if i == 0:
                gcode.append('G0 X'+str(path[i,0])+' Y'+str(path[i,1]))
            else:
                gcode.append('G1 X'+str(path[i,0])+' Y'+str(path[i,1]))

        #Save the gcode to a file
        with open('gcodeClass.gcode', 'w') as f:
            for line in gcode:
                f.write(line+'\n')
        print('Gcode saved to gcodeClass.gcode')

    def zig_zag(self, poly):
        #find the bouting box of the polygon
        minx = np.min(poly[:,0])
        maxx = np.max(poly[:,0])
        miny = np.min(poly[:,1])
        maxy = np.max(poly[:,1])
        bb = np.array([[minx,miny],[minx,maxy],[maxx,maxy],[maxx,miny]])

        #Split bb vertically with lines (number of lines = bb.width/line_distance)
        #and find the intersection points with the polygon
        #the intersection points are the start and end points of the zig-zag lines

        #find the number of lines
        n_lines = int((maxx-minx)/self.line_distance)

        #find the x coordinates of the lines
        x_lines = np.linspace(minx,maxx,n_lines)

        #find the intersection points
        points = self.bb_intersection_points(x_lines,poly)
        #construct segmentes between the points with the same x coordinate
        segments = self.construct_segments(points)
        #join the segments in a zigzag path
        path = self.join_segments_zigzag(segments)
        
        return path,segments
        
    def bb_intersection_points(self, x_lines,poly):
        points = []
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
        return points
    
    def construct_segments(self, points):
        segments = []
        for i in range(len(points)):
            if i == len(points)-1:
                if points[i][0] == points[0][0]:
                    segments.append([points[i],points[0]])
            else:
                if points[i][0] == points[i+1][0] and i%2 == 0:
                    segments.append([points[i],points[i+1]])
        return segments

    def join_segments_zigzag(self, segments):
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
        return path
        '''for i in range(len(segments)):
            if i%2 == 0:
                path.append(segments[i][0])
                path.append(segments[i][1])
            else:
                path.append(segments[i][1])
                path.append(segments[i][0])
        return path'''

def teste(self):
    pass