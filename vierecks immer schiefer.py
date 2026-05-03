import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

# Fenster einrichten
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 11)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)

# Liste, in der alle bisherigen Rechtecke gespeichert werden
rectangles = []

angle = 0          # Startwinkel
step = 0.8         # wie stark es sich jedes Mal bewegt

for i in range(25):          # wie viele Vierecke sollen erscheinen? (z.B. 25)
    # Neues Rechteck erstellen
    rect = Rectangle(
        xy=(i * step, 5),           # Position (wird immer weiter nach rechts geschoben)
        width=2, 
        height=1.5,
        angle=angle,                # immer schiefer
        color=plt.cm.viridis(i/25), # schöne Farbverlauf
        alpha=0.85,
        linewidth=1.5,
        edgecolor='black'
    )
    
    ax.add_patch(rect)
    rectangles.append(rect)
    
    # Winkel erhöhen → wird immer schiefer
    angle += 12                    # Grad pro Schritt (kannst du ändern)
    
    # Titel + Text aktualisieren
    plt.title(f'Schiefe Vierecke Animation – Schritt {i+1}', fontsize=14)
    
    # Kurze Pause damit man es gut sehen kann
    plt.pause(0.15)                # langsamer = 0.3, schneller = 0.08

plt.title('Fertig! Alle schiefen Vierecke bleiben sichtbar', fontsize=14, color='darkred')
plt.show()