#TODO: add comments
import numpy as np

import matplotlib.pyplot as plt

#TODO: Generate a offset in the segments to make the zig-zag path
#TODO: organize the variables in objects to make it more readable
#TODO: organize in functions

class Slicer:
    def __init__(self, nozzle=0.4, line_distance=1):
        self.nozzle = nozzle
        self.line_distance = line_distance*self.nozzle
        self.extrudion_rate = -0.25
        self.feed_rate = 1000
        self.poly = []
        self.paths = []

    def path2Gcode(self, paths):
        gcode = ['M302 P1; disable cold extrusion checking',
                 'M82; modo de extrusao absoluta',
                 'G92 E0 ; Reseta Extrusora',
                 'G28 X Y;',
                 'G29; Auto bed leveling',
                 'G92 E0 ; Reseta Extrusora',
                 ]
        Z = 0.2
        extruder_pos = 0
        #TODO: Add layer change and z coordinate
        for path in paths:
            #TODO: Conectar os diferentes segmentos
            #A principio o nao existe extrusao entre diferentes segmentos
            for segment in path:
                #if first segment of the path move to the start point
                if segment == path[0]:
                    gcode.append('G1 X{} Y{} Z{} F{}'.format(segment[0][0],segment[0][1],Z,self.feed_rate)) #TODO: testar feed rate
                extruder_pos += self.extrudion_rate*np.sqrt((segment[0][0]-segment[1][0])**2+(segment[0][1]-segment[1][1])**2)
                gcode.append('G1 X{} Y{} Z{} E{}'.format(segment[1][0],segment[1][1],Z,extruder_pos))
        #Save the gcode to a file
        with open('testeHJ.gcode', 'w') as f:
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
        
        array_of_seg = self.separated_segments(points)
        # join the segmentes in evry array in a zig-zag path
        paths = []
        for i in range(len(array_of_seg)):
            path_seg = self.join_segments_zigzag(array_of_seg[i])
            paths.append(path_seg)
        
        segments = self.construct_segments(points)

        #join the segments in a zigzag path
        path = self.join_segments_zigzag(segments)
        
        return paths,segments
        
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

    def separated_segments(self, points):
        # This way the zig-zag path will be more organized
        # after reconnecting the path without extrusion in between the different parts

        # Create an array with all the x coordinates of the intersection points
        x_points = [p[0] for p in points]
        # remove dupes 
        no_dupes = list(set(x_points))
        # sort no_dupes
        no_dupes.sort()
        final_array = []

        for x in no_dupes:
            # Find the number of intersection points with the same x coordinate
            n_points = x_points.count(x)
            # If it is the first time in the loop, set p_n_points to n_points and create arrays for the segments
            if x == x_points[0]:
                print("fitst")
                p_n_points = n_points
                number_of_arrays = int(n_points/2)
                arrays = [[] for _ in range(number_of_arrays)]

            # If the number of intersection points with the same x coordinate is different from the previous one,
            # create a new array for the segments in this part of the polygon
            if n_points != p_n_points:
                print("different")
                # Add the arrays to the final array
                final_array.extend(arrays)
                # Create new arrays for the segments in this part of the polygon
                number_of_arrays = int(n_points/2)
                arrays = [[] for _ in range(number_of_arrays)]
                # Set p_n_points to n_points
                p_n_points = n_points
            #create an array with all the points in the same x coordinate
            x_array = [p for p in points if p[0] == x]
            counter = 0
            for i in range(len(x_array)):
                if i != len(x_array)-1:
                    if x_array[i][0] == x_array[i+1][0] and i%2==0:
                        arrays[counter].append([x_array[i],x_array[i+1]])
                        counter +=1
            # If this is the last x coordinate, add the arrays to the final array
            if x == x_points[-1]:
                print("final")
                final_array.extend(arrays)
        
        return final_array


if __name__ == '__main__':
    # create square inside a square
    # poly = np.array([[0,0],[0,10],[10,10],[10,8],[10,0]])
    poly = np.array([[0,0],[0,10],[10,10],[10,8],[1.25,8],[1.25,6],[10,6],[10,4],[3,4],[3,2],[10,2],[10,0]])

    #rotate polygon 45 degrees
    # theta = np.radians(45)
    # theta = np.radians(90) #problema rotacionando 90 graus
    # c, s = np.cos(theta), np.sin(theta)
    # R = np.array(((c,-s), (s, c)))
    # poly = np.dot(poly,R)


    sliced = Slicer(0.4,0.8)

    paths,segments = sliced.zig_zag(poly)
    print(len(paths))
    sliced.path2Gcode(paths)
    
    plt.plot(poly[:,0],poly[:,1])
    # plt.plot([p[0] for p in points],[p[1] for p in points],'o')
    #plot path
    plt.figure()
    
    colors = ['r','g','b','y','c','m','k','w']
    i=0
    for path in paths:
        #make each path one color
        i +=1
        if i == len(colors):
            i = 0
        for segment in path:
            plt.plot([segment[0][0],segment[1][0]],[segment[0][1],segment[1][1]],color = colors[i])
            #color each segment a different color


    plt.show()  