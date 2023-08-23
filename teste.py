import numpy as np

def coordinates_to_gcode(coordinates, feed_rate, height = 1, layer_height=0.2, z_offset=2):
    gcode = ""

    # Add headers
    headers = [
        'M302 P1; disable cold extrusion checking',
        'M82; modo de extrusao absoluta',
        'G92 E0 ; Reseta Extrusora',
        'G28;',
        'G29; Auto bed leveling',
        'G92 E0 ; Reseta Extrusora',
        'G1 F{};'.format(feed_rate)
    ]
    gcode += "\n".join(headers) + "\n\n"
    e = 0
    # Iterate through each coordinate pair
    z_vals = np.arange(0, height, layer_height)
    z_vals = np.append(z_vals, height)
    
    for z in z_vals:
        for i, coord in enumerate(coordinates):
            x, y = coord
            # Move to the starting point of the path
            if i == 0:
                gcode += f"G1 X{round(x,4)} Y{round(y,4)} Z{round(z+z_offset,4)};\n"  # Rapid move
            else:
                e += -0.25*np.sqrt((coordinates[i-1][0]-x)**2+(coordinates[i-1][1]-y)**2)
                gcode += f"G1 X{round(x,4)} Y{round(y,4)} E{round(e,4)};\n"  # Linear move

        gcode += "\n"

    # Add footer
    footer = [
        'G92 E0 ; Reseta Extrusora',
        f'G1 Z{height+1}; Move Z para o fim',
        'G28 X0 Y0; Move X/Y para o fim',
        'M84; Desliga motores',
    ]

    gcode += "\n".join(footer)

    return gcode




poly = np.array([[0,0],[0,20],[20,20],[20,0],[0,0]])
poly = poly + 90

feed_rate = 300  # Set the desired feed rate


# Define the square points
# define the starting point
square_points = np.array([[0, 0]])
square_side = 20

# Calculate the radius of the circles
radius_1 = 0.25
radius_2 = 0.5
radius_3 = 0.75


# 1/4 of a circle
theta = np.linspace(0, np.pi / 2, 100)
theta_1 = np.linspace(-np.pi / 2, 0, 100)
theta_2 = np.linspace(0, np.pi / 2, 100)
theta_3 = np.linspace(np.pi / 2, np.pi, 100)

# Calculate the points on the circle
# the bottom right corner
circle_points_1 = np.array([(radius_1 * np.cos(theta_1))+(square_side-radius_1), (radius_1 * np.sin(theta_1))+radius_1]).T

#the top right corner
circle_points_2 = np.array([(radius_2 * np.cos(theta_2))+(square_side-radius_2), (radius_2 * np.sin(theta_2))+(square_side-radius_2)]).T

#the top left corner
circle_points_3 = np.array([(radius_3 * np.cos(theta_3))+radius_3, (radius_3 * np.sin(theta_3))+(square_side-radius_3)]).T


# Combine the square points and circle points
Test_square = np.concatenate([square_points, circle_points_1, circle_points_2, circle_points_3,np.array([[0,0]])])

poly = Test_square

gcode_path = coordinates_to_gcode(poly, feed_rate)

# Save G-code to a file
filename = r"testesCirculos/Teste_quadrado.gcode"
with open(filename, "w") as file:
    file.write(gcode_path)

print(f"G-code path saved to {filename}")
