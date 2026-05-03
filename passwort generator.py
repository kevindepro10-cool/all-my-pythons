import secrets
import string
import argparse


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """
    Generiert ein sicheres Passwort.

    Args:
        length:            Länge des Passworts
        use_uppercase:     Großbuchstaben einschließen
        use_lowercase:     Kleinbuchstaben einschließen
        use_digits:        Ziffern einschließen
        use_symbols:       Sonderzeichen einschließen
        exclude_ambiguous: Mehrdeutige Zeichen ausschließen (0, O, l, 1, I)

    Returns:
        Generiertes Passwort als String
    """
    alphabet = ""
    required_chars = []

    ambiguous = set("0Ol1I")

    if use_uppercase:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in ambiguous)
        alphabet += chars
        required_chars.append(secrets.choice(chars))

    if use_lowercase:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in ambiguous)
        alphabet += chars
        required_chars.append(secrets.choice(chars))

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in ambiguous)
        alphabet += chars
        required_chars.append(secrets.choice(chars))

    if use_symbols:
        chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        alphabet += chars
        required_chars.append(secrets.choice(chars))

    if not alphabet:
        raise ValueError("Mindestens eine Zeichenkategorie muss ausgewählt sein.")

    if length < len(required_chars):
        raise ValueError(
            f"Passwortlänge muss mindestens {len(required_chars)} sein,"
            f" da {len(required_chars)} Kategorien aktiviert sind."
        )

    # Restliche Zeichen zufällig füllen
    remaining = [secrets.choice(alphabet) for _ in range(length - len(required_chars))]

    # Alles zusammenmischen
    password_list = required_chars + remaining
    secrets.SystemRandom().shuffle(password_list)

    return "".join(password_list)


def check_strength(password: str) -> str:
    """Bewertet die Stärke eines Passworts."""
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if any(c in string.ascii_uppercase for c in password):
        score += 1
    if any(c in string.ascii_lowercase for c in password):
        score += 1
    if any(c in string.digits for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
        score += 1

    if score <= 3:
        return "⚠️  Schwach"
    elif score <= 5:
        return "🟡 Mittel"
    elif score <= 6:
        return "🟢 Stark"
    else:
        return "✅ Sehr stark"


def main():
    parser = argparse.ArgumentParser(
        description="🔐 Sicherer Passwort-Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python passwort_generator.py
  python passwort_generator.py -l 20
  python passwort_generator.py -l 12 --no-symbols
  python passwort_generator.py -l 24 --no-symbols --exclude-ambiguous -n 5
        """,
    )
    parser.add_argument("-l", "--length",    type=int, default=16,        help="Passwortlänge (Standard: 16)")
    parser.add_argument("-n", "--count",     type=int, default=1,         help="Anzahl der Passwörter (Standard: 1)")
    parser.add_argument("--no-uppercase",    action="store_true",         help="Keine Großbuchstaben")
    parser.add_argument("--no-lowercase",    action="store_true",         help="Keine Kleinbuchstaben")
    parser.add_argument("--no-digits",       action="store_true",         help="Keine Ziffern")
    parser.add_argument("--no-symbols",      action="store_true",         help="Keine Sonderzeichen")
    parser.add_argument("--exclude-ambiguous", action="store_true",       help="Mehrdeutige Zeichen ausschließen (0, O, l, 1, I)")

    args = parser.parse_args()

    print("\n🔐 Passwort-Generator")
    print("=" * 40)
    print(f"  Länge:              {args.length}")
    print(f"  Großbuchstaben:     {'Nein' if args.no_uppercase else 'Ja'}")
    print(f"  Kleinbuchstaben:    {'Nein' if args.no_lowercase else 'Ja'}")
    print(f"  Ziffern:            {'Nein' if args.no_digits else 'Ja'}")
    print(f"  Sonderzeichen:      {'Nein' if args.no_symbols else 'Ja'}")
    print(f"  Mehrdeutige ausschl.: {'Ja' if args.exclude_ambiguous else 'Nein'}")
    print("=" * 40)

    for i in range(args.count):
        pw = generate_password(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous,
        )
        strength = check_strength(pw)
        if args.count > 1:
            print(f"  [{i+1:02d}] {pw}  {strength}")
        else:
            print(f"\n  Passwort: {pw}")
            print(f"  Stärke:   {strength}")

    print()


if __name__ == "__main__":
    main()