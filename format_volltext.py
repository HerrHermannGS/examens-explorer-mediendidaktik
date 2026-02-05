#!/usr/bin/env python3
"""
Formatiert den Volltext der Aufgaben für bessere Lesbarkeit
"""

import json
import re
from pathlib import Path

def format_volltext(text):
    """Formatiert Volltext mit Absätzen und Strukturierung"""

    # 1. Füge Absatz vor Aufgabennummern (1., 2., 3., etc.)
    text = re.sub(r'(\s+)(\d+)\.\s+([A-ZÄÖÜ])', r'\n\n\2. \3', text)

    # 2. Füge Absatz nach Zitaten (Quelle in Klammern)
    text = re.sub(r'(\([^)]+,\s*\d{4}\))\s+', r'\1\n\n', text)

    # 3. Füge Absatz nach Einleitung (vor erster Aufgabe)
    # Suche nach dem Pattern: "Text... gewinnen. 1." oder ähnlich
    text = re.sub(r'([.!?])\s+(1\.)', r'\1\n\n\2', text, count=1)

    # 4. Entferne mehrfache Leerzeilen
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 5. Entferne Leerzeichen am Anfang und Ende
    text = text.strip()

    return text


def format_all_aufgaben():
    """Formatiert alle Aufgaben und speichert sie"""

    base_dir = Path(__file__).parent
    input_file = base_dir / 'data' / 'aufgaben_parsed.json'

    # Lade Aufgaben
    with open(input_file, 'r', encoding='utf-8') as f:
        aufgaben = json.load(f)

    print(f"📝 Formatiere {len(aufgaben)} Aufgaben...\n")

    # Formatiere Volltext
    for i, aufgabe in enumerate(aufgaben, 1):
        original = aufgabe['volltext']
        formatted = format_volltext(original)
        aufgabe['volltext'] = formatted

        # Zeige Beispiel für erste 3 Aufgaben
        if i <= 3:
            print(f"{'='*60}")
            print(f"Aufgabe {i}: {aufgabe['titel']}")
            print(f"{'='*60}")
            print(formatted[:300] + "..." if len(formatted) > 300 else formatted)
            print()

    # Speichere
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(aufgaben, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Alle Aufgaben formatiert und gespeichert!")
    print(f"💾 Datei: {input_file}")


if __name__ == '__main__':
    format_all_aufgaben()
