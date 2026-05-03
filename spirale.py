import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(8,8))
ax = plt.gca()
ax.set_facecolor('black')
plt.axis("off")

t = np.linspace(0, 20*np.pi, 4000)

def gnerate_spriral(frame):
    scale = 1 + frame * 0.02
    
    x1 = scale * t * np.cos(t + frame*0.02)
    y1 = scale * t * np.sin(t + frame*0.02)
    
    x2 = scale * t * np.sin(3*t + frame*0.03)
    y2 = scale * t * np.cos(5*t + frame*0.03)
    
    x3 = scale * t * np.cos(t*2 + frame*0.04) * np.exp(0.05*t)
    y3 = scale * t * np.sin(t*2 + frame*0.04) * np.exp(0.05*t)
    
    return x1, y1, x2, y2, x3, y3

line1, = plt.plot([], [], linewidth=0.5)
line2, = plt.plot([], [], linewidth=0.5)
line3, = plt.plot([], [], linewidth=0.5)


def animate(frame):
    x1, y1, x2, y2, x3, y3 = gnerate_spriral(frame)
    line1.set_data(x1, y1)
    line2.set_data(x2, y2)
    line3.set_data(x3, y3)
    
    ax.set_xlim(-150,150)
    ax.set_ylim(-150,150)
    
    return line1, line2, line3

ani = FuncAnimation(
    fig,
    animate,
    frames=300,
    interval=30,
    blit=True
)

plt.show()
