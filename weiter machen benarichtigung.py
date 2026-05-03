import tkinter as tk
from tkinter import font as tkfont

def show_motivation():
    # Hauptfenster erstellen
    root = tk.Tk()
    root.title("Motivation")
    
    # "Cooler Style": Rahmenloses Fenster und immer im Vordergrund
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    
    # Hintergrundfarbe (Dark Mode Design)
    bg_color = "#121212"  # Sehr dunkles Grau
    accent_color = "#00F5FF" # Neon Cyan
    text_color = "#FFFFFF"   # Weiß
    
    root.configure(bg=bg_color)
    
    # Fenstergröße und Position (Mittig auf dem Bildschirm)
    width = 450
    height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Schicker Rahmen durch ein zweites Frame
    border_frame = tk.Frame(root, bg=accent_color, bd=0)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", width=width, height=height)
    
    inner_frame = tk.Frame(border_frame, bg=bg_color, bd=0)
    inner_frame.place(relx=0.5, rely=0.5, anchor="center", width=width-4, height=height-4)

    # Schriftarten definieren
    title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
    button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

    # Nachricht
    label = tk.Label(
        inner_frame, 
        text="PROGRAMMIER WEITER,\nDAS SCHAFFST DU!", 
        fg=accent_color, 
        bg=bg_color, 
        font=title_font,
        pady=20
    )
    label.pack(expand=True)

    # Cool gestalteter Button zum Schließen
    def on_enter(e):
        btn.config(bg=accent_color, fg=bg_color)

    def on_leave(e):
        btn.config(bg=bg_color, fg=accent_color)

    btn = tk.Button(
        inner_frame, 
        text="WIRD GEMACHT!", 
        command=root.destroy,
        bg=bg_color,
        fg=accent_color,
        activebackground=accent_color,
        activeforeground=bg_color,
        font=button_font,
        bd=2,
        relief="flat",
        highlightthickness=2,
        highlightbackground=accent_color,
        padx=20,
        pady=10,
        cursor="hand2"
    )
    btn.pack(pady=(0, 20))
    
    # Hover-Effekte für den Button
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    show_motivation()
