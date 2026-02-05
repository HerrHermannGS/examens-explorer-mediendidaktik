#!/usr/bin/env python3
"""
Fügt Thementitel zu den Aufgaben hinzu und baut HTML neu
"""

import json
from pathlib import Path

def add_titles_to_aufgaben():
    """Fügt Titel aus operatoren_detailliert.json zu aufgaben_parsed.json hinzu"""

    base_dir = Path(__file__).parent

    # Lade Dateien
    with open(base_dir / 'data' / 'aufgaben_parsed.json', 'r', encoding='utf-8') as f:
        aufgaben = json.load(f)

    with open(base_dir / 'data' / 'operatoren_detailliert.json', 'r', encoding='utf-8') as f:
        operatoren_detailliert = json.load(f)

    # Baue Lookup-Table
    titel_map = {}
    for op_data in operatoren_detailliert:
        key = f"{op_data['jahr']}_{op_data['termin']}_T{op_data['thema_nr']}"
        titel_map[key] = op_data['titel']

    # Füge Titel hinzu
    updated = 0
    for aufgabe in aufgaben:
        # Extrahiere Jahr und Termin aus Semester
        parts = aufgabe['semester'].split()
        if len(parts) == 2:
            termin = parts[0]  # "Frühjahr" oder "Herbst"
            jahr = parts[1]    # "2015"
            key = f"{jahr}_{termin}_T{aufgabe['thema_nr']}"

            if key in titel_map:
                aufgabe['titel'] = titel_map[key]
                updated += 1
                print(f"✅ {key}: {titel_map[key]}")
            else:
                aufgabe['titel'] = f"Thema {aufgabe['thema_nr']}"
                print(f"⚠️  {key}: Kein Titel gefunden, verwende Standard")

    # Speichere aktualisierte Aufgaben
    with open(base_dir / 'data' / 'aufgaben_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(aufgaben, f, ensure_ascii=False, indent=2)

    print(f"\n💾 {updated}/{len(aufgaben)} Aufgaben mit Titeln aktualisiert")
    print(f"✅ Gespeichert: data/aufgaben_parsed.json")

if __name__ == '__main__':
    add_titles_to_aufgaben()
