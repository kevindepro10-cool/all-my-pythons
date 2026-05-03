import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.axis('off')

plt.title('Doppel-Spirale – leuchtend & dicht', fontsize=16, color='white', pad=30)

for i in range (350):
    radius = i * 0.085
    angle1 = i * 0.18
    angle2 = -i * 0.18
    
    x1 = radius * np.cos(angle1)
    y1 = radius * np.sin(angle1)
    ax.plot(x1, y1, 'o', color=plt.cm.plasma(i/350), markersize=5, alpha=0.9)
    
    x2 = radius * np.cos(angle2)
    y2 = radius * np.sin(angle2)
    ax.plot(x2, y2, 'o', color=plt.cm.viridis(i/350), markersize=5, alpha=0.9)
    
    if i % 8 == 0:
        plt.pause(0.015)
        
plt.title('Fertig – Schöne doppelte leuchtende Spirale!', fontsize=15, color='cyan')
plt.show()