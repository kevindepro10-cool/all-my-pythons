#!/usr/bin/env python3
"""
QR-Code Ersteller
Verwendung: python qrcode_ersteller.py
"""

import os
import sys

import qrcode
from PIL import ImageColor                               # Fix 1: Import auf Modulebene
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def erstelle_qrcode(
    inhalt: str,
    dateiname: str = "qrcode.png",
    version: int = None,
    fehlerkorrektur: str = "H",
    box_size: int = 10,
    rahmen: int = 4,
    farbe_vordergrund: str = "black",
    farbe_hintergrund: str = "white",
    abgerundet: bool = False,
) -> str:
    """
    Erstellt einen QR-Code und speichert ihn als Bild.

    Args:
        inhalt:             Text, URL oder Daten für den QR-Code
        dateiname:          Name der Ausgabedatei (.png)
        version:            QR-Code-Version 1–40 (None = automatisch)
        fehlerkorrektur:    L (7%), M (15%), Q (25%), H (30%)
        box_size:           Pixel pro Modul (>= 1)
        rahmen:             Breite des Rahmens in Modulen (>= 0)
        farbe_vordergrund:  Farbe der dunklen Module (z. B. "black", "#1a1a2e")
        farbe_hintergrund:  Farbe des Hintergrunds (z. B. "white", "#f0f0f0")
        abgerundet:         Abgerundete Module statt Quadrate

    Returns:
        Pfad zur gespeicherten Datei
    """

    # Inhalt prüfen
    if not inhalt or not inhalt.strip():
        raise ValueError("❌ Inhalt darf nicht leer sein.")

    # Version prüfen – Fix 3: Typ- und Wertebereich-Prüfung
    if version is not None:
        if not isinstance(version, int):
            raise ValueError(f"❌ Version muss eine ganze Zahl sein (1–40), nicht '{type(version).__name__}'.")
        if not (1 <= version <= 40):
            raise ValueError(f"❌ Ungültige Version '{version}'. Erlaubt: 1–40 oder None (automatisch).")

    # Fehlerkorrektur-Level prüfen – Fix 2: None-Check vor .upper()
    if fehlerkorrektur is None or not isinstance(fehlerkorrektur, str):
        raise ValueError("❌ Fehlerkorrektur muss ein String sein: L, M, Q oder H.")
    fehler_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    if fehlerkorrektur.upper() not in fehler_map:
        raise ValueError(f"❌ Ungültiger Fehlerkorrektur-Level '{fehlerkorrektur}'. Erlaubt: L, M, Q, H.")
    fehler_level = fehler_map[fehlerkorrektur.upper()]

    # box_size und rahmen prüfen – Fix 4, 5, 7
    if not isinstance(box_size, int) or box_size < 1:
        raise ValueError(f"❌ box_size muss eine ganze Zahl >= 1 sein (war: '{box_size}').")
    if not isinstance(rahmen, int) or rahmen < 0:
        raise ValueError(f"❌ rahmen muss eine ganze Zahl >= 0 sein (war: '{rahmen}').")

    # Farben prüfen
    for farbe, name in [(farbe_vordergrund, "Vordergrund"), (farbe_hintergrund, "Hintergrund")]:
        try:
            ImageColor.getrgb(farbe)
        except (ValueError, AttributeError):
            raise ValueError(f"❌ Ungültige {name}-Farbe: '{farbe}'. Beispiele: 'black', '#1a1a2e', 'red'.")

    # Dateiendung sicherstellen
    if not dateiname.lower().endswith(".png"):
        dateiname += ".png"

    # Ausgabeverzeichnis prüfen – Fix 6
    ausgabe_verzeichnis = os.path.dirname(os.path.abspath(dateiname))
    if not os.path.isdir(ausgabe_verzeichnis):
        raise ValueError(f"❌ Verzeichnis existiert nicht: '{ausgabe_verzeichnis}'.")

    qr = qrcode.QRCode(
        version=version,
        error_correction=fehler_level,
        box_size=box_size,
        border=rahmen,
    )
    qr.add_data(inhalt)
    qr.make(fit=True)

    # Bild erstellen
    if abgerundet:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color=farbe_vordergrund,
            back_color=farbe_hintergrund,
        )
    else:
        img = qr.make_image(
            fill_color=farbe_vordergrund,
            back_color=farbe_hintergrund,
        )

    img.save(dateiname)
    print(f"✅ QR-Code gespeichert: {os.path.abspath(dateiname)}")
    print(f"   Inhalt:  {inhalt}")
    print(f"   Version: {qr.version}  |  Größe: {img.size[0]}x{img.size[1]} px")
    return dateiname


def interaktiver_modus():
    """Führt den Benutzer interaktiv durch die QR-Code-Erstellung."""
    print("=" * 50)
    print("        QR-CODE ERSTELLER  🔲")
    print("=" * 50)

    # Inhalt
    inhalt = input("\nInhalt (URL, Text, E-Mail …): ").strip()
    if not inhalt:
        print("❌ Kein Inhalt eingegeben. Abbruch.")
        sys.exit(1)

    # Dateiname
    dateiname = input("Dateiname [qrcode.png]: ").strip() or "qrcode.png"

    # Farben
    print("\nFarben (leer lassen für Standard):")
    fg = input("  Vordergrund [black]: ").strip() or "black"
    bg = input("  Hintergrund [white]: ").strip() or "white"

    # Stil
    abgerundet_input = input("\nAbgerundete Module? (j/N): ").strip().lower()
    abgerundet = abgerundet_input in ("j", "ja", "y", "yes")

    # Fehlerkorrektur
    print("\nFehlerkorrektur-Level:")
    print("  L = 7%  |  M = 15%  |  Q = 25%  |  H = 30% (Standard)")
    fk = input("Auswahl [H]: ").strip().upper() or "H"

    print()
    try:                                                 # Fix 8: ValueError abfangen
        erstelle_qrcode(
            inhalt=inhalt,
            dateiname=dateiname,
            fehlerkorrektur=fk,
            farbe_vordergrund=fg,
            farbe_hintergrund=bg,
            abgerundet=abgerundet,
        )
    except ValueError as e:
        print(e)
        sys.exit(1)


# ── Beispiele direkt ausführbar ──────────────────────────────────────────────

def beispiele():
    """Erstellt einige Demo-QR-Codes."""
    erstelle_qrcode("https://www.example.com", "beispiel_url.png")
    erstelle_qrcode("Hallo Welt! 👋", "beispiel_text.png", farbe_vordergrund="#1a1a2e", farbe_hintergrund="#e8f4f8")
    erstelle_qrcode("mailto:info@example.com", "beispiel_email.png", abgerundet=True)
    erstelle_qrcode("BEGIN:VCARD\nFN:Max Mustermann\nTEL:+4912345678\nEND:VCARD", "beispiel_vcard.png")


# ── Einstiegspunkt ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            # Schnellmodus: python qrcode_ersteller.py "https://..."
            erstelle_qrcode(sys.argv[1])
        elif len(sys.argv) >= 3:
            # Schnellmodus mit Dateiname: python qrcode_ersteller.py "Text" datei.png
            erstelle_qrcode(sys.argv[1], sys.argv[2])
        else:
            # Interaktiver Modus
            interaktiver_modus()
    except ValueError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
        sys.exit(0)