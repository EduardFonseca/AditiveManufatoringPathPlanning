import plotly.graph_objects as go
import numpy as np

# define the region
x = np.linspace(-100,500,100)
y=x
y1 = (600-2*x)/1
y2 = (1000-3*x)/2
y3 = 300 - 0*x
y4 = 0*x
x1 = 400 - 0*y
x2 = 0*y

# find the intersection points
x_intersect = [0,300,200,400/3,0]
y_intersect = [0,0,200,300,300]

# plot the region
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_intersect,
                         y=y_intersect,
                         fill='toself', fillcolor='blue', opacity=0.2, name='Feasible Region'))
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='2A + B <= 600'))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='3A + 2B <= 1000'))
fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='B <=300'))
fig.add_trace(go.Scatter(x=x, y=y4, mode='lines', name='B >= 0'))
fig.add_trace(go.Scatter(x=x1, y=y, mode='lines', name='A <= 400'))
fig.add_trace(go.Scatter(x=x2, y=y, mode='lines', name='A >= 0'))

# Set the plot layout
fig.update_layout(title='Regiao possivel para a solucao',
                  xaxis_title='A',
                  yaxis_title='B',
                  xaxis_range=[-100, 450],
                  yaxis_range=[-100, 350],
                  showlegend=True)

# define the constraints
fig.show()
