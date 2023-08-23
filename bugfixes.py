import plotly.graph_objects as go
import numpy as np

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

# Create the figure
fig = go.Figure()

#plot all_points
# make axis go from -90 to 90
fig.update_xaxes(range=[-5, 25])
fig.update_yaxes(range=[-5, 25])
fig.add_trace(go.Scatter(x=Test_square[:, 0], y=Test_square[:, 1], marker=dict(size=10)))
# fig.add_trace(go.Scatter(x=circle_points_1[:, 0], y=circle_points_1[:, 1], marker=dict(size=10)))

#show the figure
fig.show()
