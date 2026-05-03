import turtle
import time

def create_building_circle():
    # Setup des Fensters
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("black")
    screen.title("Building Circle Animation")
    screen.tracer(0)  # Schaltet automatische Updates aus für flüssigere Animation

    # Setup der Schildkröte (Artist)
    artist = turtle.Turtle()
    artist.hideturtle()
    artist.pensize(4)
    
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FFFF33", "#33FFFF"]
    color_index = 0
    radius = 150

    try:
        while True:
            # Für jeden Durchlauf bauen wir den Kreis von 0 bis 360 Grad auf
            for angle in range(0, 361, 4):
                artist.clear()
                artist.penup()
                
                # Positioniere die Schildkröte so, dass der Kreis zentriert ist
                artist.goto(0, -radius)
                artist.setheading(0)
                artist.color(colors[color_index])
                artist.pendown()
                
                # Zeichne den Teil des Kreises (Extent)
                artist.circle(radius, extent=angle)
                
                # Manuelles Update des Bildschirms
                screen.update()
                time.sleep(0.01)
            
            # Farbe für den nächsten Durchlauf wechseln
            color_index = (color_index + 1) % len(colors)
            time.sleep(0.2)
            
    except turtle.Terminator:
        # Erlaubt das Schließen des Fensters ohne Fehlermeldung
        pass

if __name__ == "__main__":
    create_building_circle()
