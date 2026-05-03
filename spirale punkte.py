import matplotlib.pyplot as plt
import numpy as np
from time import sleep

# Fenster einrichten
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.axis('off')

plt.title('Wachsende leuchtende Spirale', fontsize=16, color='white', pad=20)

points = []   # speichert alle bisherigen Punkte

for i in range(180):          # Anzahl der Punkte (mehr = größere Spirale)
    # Spirale berechnen
    radius = i * 0.08          # wird immer größer
    angle = i * 0.22           # dreht sich stärker
    
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    
    # Neuen Punkt zeichnen
    color = plt.cm.viridis(i / 180)   # schöner Farbverlauf (grün → lila)
    point = ax.plot(x, y, 'o', color=color, markersize=6, alpha=0.95)[0]
    points.append(point)
    
    # Kurze Pause für Animation
    plt.pause(0.03)
    
    # Titel mit Zähler
    if i % 20 == 0:
        plt.title(f'Spirale wächst... {i} Punkte', fontsize=15, color='white')

plt.title('Fertig! Schöne leuchtende Spirale', fontsize=16, color='cyan')
plt.show()