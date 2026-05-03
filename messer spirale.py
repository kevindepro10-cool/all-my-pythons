import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_knife_spiral(num_knives=60, rotations=3):
    """
    Erstellt eine grafische Darstellung einer Spirale aus Messern.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    
    fig.patch.set_facecolor('#f0f0f0')

    theta = np.linspace(0.5, rotations * 2 * np.pi, num_knives)
    r = 0.5 * theta
    
    for i in range(num_knives):
        t = theta[i]
        dist = r[i]
        
        x = dist * np.cos(t)
        y = dist * np.sin(t)
        
        blade_coords = np.array([
            [0.0, 0.0],    
            [0.1, -0.8],   
            [-0.02, -0.8], 
        ])
        
        handle_coords = np.array([
            [0.06, -0.8],
            [0.06, -1.1],
            [-0.02, -1.1],
            [-0.02, -0.8]
        ])
        
        scale = 0.3 + (dist * 0.1)
        
        angle = t + np.pi/2 
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
        
        def transform(coords):
            return (coords * scale) @ rotation_matrix.T + [x, y]

        blade = Polygon(transform(blade_coords), closed=True, 
                        facecolor='silver', edgecolor='gray', linewidth=1, zorder=3)
        handle = Polygon(transform(handle_coords), closed=True, 
                         facecolor='#4b2c20', edgecolor='black', linewidth=1, zorder=2)
        
        ax.add_patch(blade)
        ax.add_patch(handle)

    limit = max(r) + 2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    plt.title("Messer-Spirale", fontsize=15, pad=20, color='#333333')
    plt.show()

if __name__ == "__main__":
    draw_knife_spiral(num_knives=50, rotations=2.5) # type: ignore
