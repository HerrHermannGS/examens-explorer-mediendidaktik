#!/usr/bin/env python3
"""
Parst die Übersichts-PDF und ordnet Stichpunkte den Aufgaben zu
"""

import json
import re
from pathlib import Path
from pypdf import PdfReader

def parse_overview_pdf():
    """Extrahiert Themenliste aus der Übersichts-PDF"""

    reader = PdfReader('data/Alte Themen Didadktik und Erzieziehung Examen.pdf')

    # Extrahiere kompletten Text
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # Finde "Mediendidaktik" Sektion
    mediendidaktik_match = re.search(r'Mediendidaktik\s*\n\s*Zeitraum\s+Thema 1\s+Thema 2(.+)', full_text, re.DOTALL)

    if not mediendidaktik_match:
        print("❌ Mediendidaktik-Sektion nicht gefunden!")
        return {}

    mediendidaktik_text = mediendidaktik_match.group(1)

    # Parse Einträge
    # Format: "2025 F Titel1\nStichpunkte\nTitel2\nStichpunkte"
    themen_dict = {}

    # Pattern für Zeitraum-Zeilen: "2025 F" oder "2024 H"
    lines = mediendidaktik_text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Prüfe ob Zeitraum (z.B. "2025 F" oder "2024 H")
        zeitraum_match = re.match(r'^(20\d{2})\s+([FH])', line)

        if zeitraum_match:
            jahr = zeitraum_match.group(1)
            termin = "Frühjahr" if zeitraum_match.group(2) == "F" else "Herbst"

            # Nächste Zeile ist Titel von Thema 1
            i += 1
            if i >= len(lines):
                break

            titel1 = lines[i].strip()
            stichpunkte1 = []

            # Sammle Stichpunkte für Thema 1
            i += 1
            while i < len(lines):
                line = lines[i].strip()

                # Wenn Zeile leer oder nächster Titel oder Zeitraum
                if not line or re.match(r'^20\d{2}\s+[FH]', line):
                    break

                # Prüfe ob das der Titel von Thema 2 ist (keine Stichpunkte)
                # Thema 2 Titel haben meist Großbuchstaben am Anfang
                if re.match(r'^[A-ZÄÖÜ]', line) and len(stichpunkte1) > 0:
                    # Das ist Titel von Thema 2
                    titel2 = line
                    stichpunkte2 = []

                    # Sammle Stichpunkte für Thema 2
                    i += 1
                    while i < len(lines):
                        line = lines[i].strip()
                        if not line or re.match(r'^20\d{2}\s+[FH]', line):
                            break
                        stichpunkte2.append(line)
                        i += 1

                    # Speichere Thema 2
                    key2 = f"{jahr}_{termin}_T2"
                    themen_dict[key2] = {
                        'titel': titel2,
                        'stichpunkte': '; '.join(stichpunkte2)
                    }
                    i -= 1  # Gehe einen Schritt zurück für äußere Schleife
                    break
                else:
                    stichpunkte1.append(line)

                i += 1

            # Speichere Thema 1
            key1 = f"{jahr}_{termin}_T1"
            themen_dict[key1] = {
                'titel': titel1,
                'stichpunkte': '; '.join(stichpunkte1)
            }

        i += 1

    return themen_dict


def add_stichpunkte_to_aufgaben():
    """Fügt Stichpunkte zu den Aufgaben hinzu"""

    base_dir = Path(__file__).parent

    # Parse Übersicht
    print("📖 Parse Übersichts-PDF...")
    themen_dict = parse_overview_pdf()

    print(f"✅ {len(themen_dict)} Themen gefunden\n")

    # Zeige erste paar Einträge
    for key, data in list(themen_dict.items())[:3]:
        print(f"{key}:")
        print(f"  Titel: {data['titel']}")
        print(f"  Stichpunkte: {data['stichpunkte'][:100]}...")
        print()

    # Lade Aufgaben
    with open(base_dir / 'data' / 'aufgaben_parsed.json', 'r', encoding='utf-8') as f:
        aufgaben = json.load(f)

    # Füge Stichpunkte hinzu
    matched = 0
    for aufgabe in aufgaben:
        parts = aufgabe['semester'].split()
        if len(parts) == 2:
            termin = parts[0]  # "Frühjahr" oder "Herbst"
            jahr = parts[1]    # "2015"
            key = f"{jahr}_{termin}_T{aufgabe['thema_nr']}"

            if key in themen_dict:
                aufgabe['stichpunkte'] = themen_dict[key]['stichpunkte']
                matched += 1
                print(f"✅ {key}: Stichpunkte zugeordnet")
            else:
                aufgabe['stichpunkte'] = ""
                print(f"⚠️  {key}: Keine Stichpunkte gefunden")

    # Speichere
    with open(base_dir / 'data' / 'aufgaben_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(aufgaben, f, ensure_ascii=False, indent=2)

    print(f"\n💾 {matched}/{len(aufgaben)} Aufgaben mit Stichpunkten aktualisiert")


if __name__ == '__main__':
    add_stichpunkte_to_aufgaben()
