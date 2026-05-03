"""
Siebenundsechzig (67) – Kartenspiel
====================================
2–4 Spieler | 24 Karten (9–As in 4 Farben)
Kartenwerte: As=11, 10=10, König=4, Dame=3, Bube=2, 9=0
Ziel: Als Erster 67 Punkte sammeln.

Regeln (vereinfacht):
  - Jeder Spieler bekommt 6 Karten.
  - Es wird reihum eine Karte gespielt (Stich-Prinzip).
  - Wer den Stich gewinnt, nimmt alle Karten und addiert deren Werte.
  - Wer zuerst 67 Punkte (kumuliert über Runden) erreicht, gewinnt.
  - Muss die gespielte Farbe bedient werden, wenn möglich.
  - Bei Gleichstand gewinnt die höhere Karte; As schlägt 10 schlägt König usw.
"""

import random

# ──────────────────────────────── Karten ────────────────────────────────

FARBEN = ["♠ Pik", "♥ Herz", "♦ Karo", "♣ Kreuz"]
WERTE  = ["9", "Bube", "Dame", "König", "10", "As"]
PUNKTE = {"9": 0, "Bube": 2, "Dame": 3, "König": 4, "10": 10, "As": 11}
RANG   = {w: i for i, w in enumerate(WERTE)}  # höherer Index = stärker


class Karte:
    def __init__(self, farbe: str, wert: str):
        self.farbe = farbe
        self.wert  = wert

    @property
    def punkte(self) -> int:
        return PUNKTE[self.wert]

    def __str__(self) -> str:
        return f"{self.farbe} {self.wert}"

    def schlaegt(self, andere: "Karte") -> bool:
        """True, wenn self die andere Karte im selben Stich schlägt."""
        if self.farbe != andere.farbe:
            return False          # andere Farbe kann nicht schlagen
        return RANG[self.wert] > RANG[andere.wert]


# ──────────────────────────────── Deck ──────────────────────────────────

def neues_deck() -> list[Karte]:
    deck = [Karte(f, w) for f in FARBEN for w in WERTE]
    random.shuffle(deck)
    return deck


# ──────────────────────────────── Spieler ───────────────────────────────

class Spieler:
    def __init__(self, name: str, ist_mensch: bool = False):
        self.name       = name
        self.ist_mensch = ist_mensch
        self.hand: list[Karte] = []
        self.punkte_gesamt = 0

    def zeige_hand(self):
        print(f"\n  Deine Karten ({self.name}):")
        for i, k in enumerate(self.hand):
            print(f"    [{i+1}] {k}  ({k.punkte} Pkt.)")

    def waehle_karte(self, angespielte_farbe: str | None) -> Karte:
        """Menschliche Eingabe: Karte wählen."""
        while True:
            self.zeige_hand()
            try:
                idx = int(input("  Welche Karte spielst du? (Nummer): ")) - 1
                if 0 <= idx < len(self.hand):
                    karte = self.hand[idx]
                    # Farb-Zwang prüfen
                    if angespielte_farbe:
                        hat_farbe = any(k.farbe == angespielte_farbe for k in self.hand)
                        if hat_farbe and karte.farbe != angespielte_farbe:
                            print(f"  ⚠ Du musst {angespielte_farbe} bedienen!")
                            continue
                    self.hand.pop(idx)
                    return karte
            except (ValueError, IndexError):
                pass
            print("  Ungültige Eingabe – bitte Nummer eingeben.")

    def ki_karte(self, angespielte_farbe: str | None) -> Karte:
        """Einfache KI: spielt höchste Karte der angespielten Farbe, sonst niedrigste."""
        if angespielte_farbe:
            passende = [k for k in self.hand if k.farbe == angespielte_farbe]
        else:
            passende = []

        pool = passende if passende else self.hand
        # KI spielt die stärkste verfügbare Karte, wenn Farbe passt; sonst schwächste
        if passende:
            karte = max(pool, key=lambda k: RANG[k.wert])
        else:
            karte = min(pool, key=lambda k: RANG[k.wert])
        self.hand.remove(karte)
        return karte


# ──────────────────────────────── Stich ─────────────────────────────────

def spiele_stich(spieler: list[Spieler], startindex: int) -> int:
    """
    Spielt einen Stich und gibt den Index des Gewinners zurück.
    """
    n = len(spieler)
    gespielte: list[tuple[int, Karte]] = []
    angespielte_farbe: str | None = None

    print("\n" + "─" * 45)
    for i in range(n):
        idx = (startindex + i) % n
        sp  = spieler[idx]

        if sp.ist_mensch:
            karte = sp.waehle_karte(angespielte_farbe)
        else:
            karte = sp.ki_karte(angespielte_farbe)
            print(f"  {sp.name} spielt: {karte}")

        if angespielte_farbe is None:
            angespielte_farbe = karte.farbe
        gespielte.append((idx, karte))

    # Gewinner ermitteln: höchste Karte der angespielten Farbe
    stich_punkte = sum(k.punkte for _, k in gespielte)
    gewinner_idx, gewinner_karte = gespielte[0]

    for idx, karte in gespielte[1:]:
        if karte.schlaegt(gewinner_karte):
            gewinner_idx, gewinner_karte = idx, karte

    spieler[gewinner_idx].punkte_gesamt += stich_punkte
    print(f"\n  → {spieler[gewinner_idx].name} gewinnt den Stich "
          f"(+{stich_punkte} Pkt., gesamt {spieler[gewinner_idx].punkte_gesamt})")
    return gewinner_idx


# ──────────────────────────────── Runde ─────────────────────────────────

def spiele_runde(spieler: list[Spieler]) -> Spieler | None:
    """Spielt eine vollständige Runde (alle Stiche). Gibt Sieger zurück oder None."""
    deck = neues_deck()

    # 6 Karten pro Spieler
    for sp in spieler:
        sp.hand = [deck.pop() for _ in range(6)]

    startindex = 0
    for stich_nr in range(6):
        print(f"\n{'═'*45}")
        print(f"  Stich {stich_nr + 1}/6")
        startindex = spiele_stich(spieler, startindex)

        # Gesamtstand
        print("\n  Punktestand:")
        for sp in spieler:
            print(f"    {sp.name:15s}: {sp.punkte_gesamt:3d} Pkt.")

        # Sieg prüfen
        for sp in spieler:
            if sp.punkte_gesamt >= 67:
                return sp

    return None


# ──────────────────────────────── Hauptprogramm ─────────────────────────

def main():
    print("╔══════════════════════════════════════════╗")
    print("║    S I E B E N U N D S E C H Z I G       ║")
    print("║            Das Kartenspiel                ║")
    print("╚══════════════════════════════════════════╝")
    print()

    # Spieleranzahl
    while True:
        try:
            n = int(input("Wie viele Spieler? (2–4): "))
            if 2 <= n <= 4:
                break
        except ValueError:
            pass
        print("Bitte 2, 3 oder 4 eingeben.")

    # Spielernamen
    spieler: list[Spieler] = []
    dein_name = input("Dein Name: ").strip() or "Du"
    spieler.append(Spieler(dein_name, ist_mensch=True))
    ki_namen = ["KI-Alex", "KI-Bert", "KI-Clara"]
    for i in range(n - 1):
        spieler.append(Spieler(ki_namen[i]))

    print(f"\nSpieler: {', '.join(sp.name for sp in spieler)}")
    print("Ziel: Als Erster 67 Punkte erreichen!\n")
    input("Drücke Enter zum Starten …")

    sieger = None
    runde  = 1
    while sieger is None:
        print(f"\n{'#'*45}")
        print(f"  RUNDE {runde}")
        sieger = spiele_runde(spieler)
        runde += 1

    print(f"\n{'★'*45}")
    print(f"  🏆  {sieger.name} gewinnt mit {sieger.punkte_gesamt} Punkten!")
    print(f"{'★'*45}\n")

    print("Endabrechnung:")
    for sp in sorted(spieler, key=lambda s: -s.punkte_gesamt):
        print(f"  {sp.name:15s}: {sp.punkte_gesamt} Pkt.")


if __name__ == "__main__":
    main()