#Generate Gcode to draw a line with constant speed and extrusion rate
#Velocidade de extrusao tem que ser 0.25 por unidade no x e y

feedRate = 1000 #mm/min
position  = [
    [0,200,0],
    [200,200,-50]
]


with open("GcodeTeste.gcode", "w") as f:
    #TODO: add header to a file
    # header
    f.write('M302 P1; disable cold extrusion checking') #disable cold extrusion checking
    f.write("M82; modo de extrusao absoluta\n") # extrusion mode absolute
    f.write("G92 E0 ; Reseta Extrusora\n") # reset extruder
    #FIXME: add a way to home z
    f.write("G28 X Y;\n")  # home X Y
    f.write("G92 E0 ; Reseta Extrusora\n") # reset extruder

    #Actual Gcode
    f.write("G1 F{};\n".format(feedRate))
    for x,y ,e in position:
        #FIXME: Extruder not moving
        f.write("G1 X{} Y{} E{};\n".format(x,y,e)) # move to position

    f.write("M104 S0 ;Turn-off hotend\n") # turn off hotend