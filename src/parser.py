#!/usr/bin/env python3
"""
Parser für Mediendidaktik Examensaufgaben
Extrahiert: Semester, Thema, Operatoren, Zitate, Themen-Kategorien
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any

# AFB-Zuordnung der Operatoren
AFB_OPERATORS = {
    'AFB I': ['nennen', 'beschreiben', 'darstellen', 'wiedergeben', 'definieren', 'aufzeigen', 'benennen'],
    'AFB II': ['erklären', 'erläutern', 'zeigen sie auf', 'begründen', 'charakterisieren', 'vergleichen',
               'gegenüberstellen', 'analysieren', 'ableiten', 'einordnen', 'stellen sie dar', 'legen sie dar'],
    'AFB III': ['diskutieren', 'erörtern', 'beurteilen', 'bewerten', 'entwerfen', 'entwickeln', 'gestalten',
                'konzipieren', 'skizzieren', 'überprüfen', 'prüfen', 'sich auseinandersetzen', 'setzen sie sich auseinander']
}

# Themen-Kategorien (nach Wichtige_Themenbereiche.png)
THEMA_KATEGORIEN = {
    'Mediendidaktische Konzepte': [
        'SAMR', 'Puentedura', 'CTML', 'Mayer', 'Designeffekte', 'Gestaltungsprinzipien',
        'Digitale Lernaufgaben', 'ICAP', 'Chi', 'Wylie', 'Multimedia'
    ],
    'Lehr-Lerntheorien': [
        'Kognitivismus', 'Konstruktivismus', 'Konnektivismus', 'Instruktional Design', 'Instructional Design',
        'Problemorientierung', 'problembasiert', 'problemorientiert', 'entdeckendes Lernen',
        'selbstreguliert', 'selbstgesteuert', 'kollaborativ', 'kooperativ', 'Projektmethode', 'SCRUM', 'Kanban',
        'Direkte Instruktion', 'Blended Learning'
    ],
    'Lernpsychologie': [
        'Cognitive Load Theory', 'CLT', 'Sweller', 'Drei-Speicher-Modell', 'Atkinson', 'Shiffrin',
        'Motivation', 'Deci', 'Ryan', 'Assimilation', 'Akkommodation', 'Feedback', 'Hattie',
        'Visual Literacy', 'Repräsentationsformen'
    ],
    'Spezifische Medien/Formate': [
        'Lernplattform', 'LMS', 'Moodle', 'mebis', 'Interactive Whiteboard', 'IWB', 'Tablet', 'Smartphone',
        'BYOD', 'WebQuest', 'Tutorial', 'Erklärvideo', 'Flipped Classroom', 'E-Portfolio',
        'Quiz', 'Abstimmungssystem', 'Gamification', 'Game-based Learning', 'AR', 'Augmented Reality',
        'VR', 'Virtual Reality', 'Podcast', 'Audio', 'auditiv', 'Visualisierung', 'Mindmap', 'Concept Map',
        'Hypertext', 'OER', 'Open Educational Resources', 'mobile Endgeräte'
    ]
}


def extract_semester(text: str) -> str:
    """Extrahiert Semester aus Dateinamen oder Text"""
    # Pattern 1: YYYY-Season oder YYYYH / YYYYF
    match = re.search(r'(\d{4})[-_]?(Frühjahr|Herbst|fruehjahr|frueh|herbst|F|H)(?:\b|_|-)', text, re.IGNORECASE)
    if match:
        year = match.group(1)
        season = match.group(2).lower()
        # Normalisiere Saison
        if season in ['frühjahr', 'fruehjahr', 'frueh', 'f']:
            season_normalized = 'Frühjahr'
        else:
            season_normalized = 'Herbst'
        return f"{year} {season_normalized}"
    return "Unbekannt"


def extract_operators(text: str) -> Dict[str, List[str]]:
    """Extrahiert Operatoren und ordnet sie AFB-Level zu"""
    text_lower = text.lower()
    found_operators = {'AFB I': [], 'AFB II': [], 'AFB III': []}

    for afb, operators in AFB_OPERATORS.items():
        for op in operators:
            # Suche nach dem Operator mit Wortgrenzen
            pattern = r'\b' + re.escape(op) + r'\b'
            if re.search(pattern, text_lower):
                # Kapitalisiere nur den ersten Buchstaben
                found_operators[afb].append(op.capitalize())

    # Deduplizieren und sortieren
    for afb in found_operators:
        found_operators[afb] = sorted(list(set(found_operators[afb])))

    return found_operators


def extract_themen(text: str) -> Dict[str, List[str]]:
    """Extrahiert Themen und ordnet sie Kategorien zu"""
    found_themen = {
        'Mediendidaktische Konzepte': [],
        'Lehr-Lerntheorien': [],
        'Lernpsychologie': [],
        'Spezifische Medien/Formate': []
    }

    for kategorie, themen_liste in THEMA_KATEGORIEN.items():
        for thema in themen_liste:
            # Case-insensitive Suche
            pattern = r'\b' + re.escape(thema) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_themen[kategorie].append(thema)

    # Deduplizieren
    for kategorie in found_themen:
        found_themen[kategorie] = list(set(found_themen[kategorie]))

    return found_themen


def extract_citations(text: str) -> List[Dict[str, str]]:
    """Extrahiert Zitate (Text + Autor/Quelle)"""
    citations = []

    # Pattern 1: (Autor, Jahr) - am häufigsten
    matches = re.finditer(r'\(([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*)[,\s]+(\d{4})\)', text)
    for match in matches:
        author = match.group(1)
        year = match.group(2)
        # Versuche, den Text vor dem Zitat zu extrahieren (bis zu 200 Zeichen zurück)
        start = max(0, match.start() - 200)
        quote_text = text[start:match.start()].strip()
        # Nimm nur die letzten 2 Sätze
        sentences = re.split(r'[.!?]\s+', quote_text)
        quote_text = '. '.join(sentences[-2:]) if len(sentences) > 1 else quote_text

        citations.append({
            'text': quote_text.strip(),
            'author': author,
            'source': f"{author}, {year}"
        })

    # Pattern 2: Quelle: ... am Anfang
    matches = re.finditer(r'Quelle:\s*([^\n]+)', text)
    for match in matches:
        source = match.group(1).strip()
        # Versuche, den Text davor zu finden
        start = max(0, match.start() - 300)
        quote_text = text[start:match.start()].strip()
        sentences = re.split(r'[.!?]\s+', quote_text)
        quote_text = '. '.join(sentences[-2:]) if len(sentences) > 1 else quote_text

        citations.append({
            'text': quote_text.strip(),
            'author': '',
            'source': source
        })

    return citations[:3]  # Maximal 3 Zitate pro Aufgabe


def count_subtasks(text: str) -> int:
    """Zählt Teilaufgaben (1., 2., 3., etc.)"""
    # Suche nach Patterns wie "1." "2." "3." am Zeilenanfang oder nach Absatz
    matches = re.findall(r'(?:^|\n)\s*(\d+)\s*\.', text)
    if matches:
        # Nimm die höchste Nummer
        return max([int(m) for m in matches])
    return 1  # Mindestens 1 Teilaufgabe


def parse_aufgaben(filepath: str) -> List[Dict[str, Any]]:
    """Hauptparser-Funktion"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    aufgaben = []

    # Splitte nach Dateien
    files = re.split(r'={80}\nDATEI: ([^\n]+)\n={80}', content)

    # Iteriere über Paare (Dateiname, Inhalt)
    for i in range(1, len(files), 2):
        if i + 1 >= len(files):
            break

        dateiname = files[i].strip()
        file_content = files[i + 1]

        # Extrahiere Semester
        semester = extract_semester(dateiname)

        # Splitte nach "Thema Nr. 1" und "Thema Nr. 2"
        themen = re.split(r'Thema Nr\.\s*([12])', file_content)

        # Thema 1
        if len(themen) >= 3:
            thema_nr = themen[1]
            thema_text = themen[2]

            # Finde das Ende von Thema 1 (entweder bei Thema 2 oder Ende)
            if len(themen) >= 5:
                # Es gibt Thema 2, also schneide bei "Thema Nr. 2" ab
                thema_text = thema_text.split('Thema Nr.')[0]

            aufgabe_id = f"{semester.replace(' ', '_')}_T1"
            aufgaben.append({
                'id': aufgabe_id,
                'semester': semester,
                'thema_nr': 1,
                'operatoren': extract_operators(thema_text),
                'themen': extract_themen(thema_text),
                'zitate': extract_citations(thema_text),
                'teilaufgaben_anzahl': count_subtasks(thema_text),
                'volltext': thema_text.strip()
            })

        # Thema 2
        if len(themen) >= 5:
            thema_nr = themen[3]
            thema_text = themen[4]

            aufgabe_id = f"{semester.replace(' ', '_')}_T2"
            aufgaben.append({
                'id': aufgabe_id,
                'semester': semester,
                'thema_nr': 2,
                'operatoren': extract_operators(thema_text),
                'themen': extract_themen(thema_text),
                'zitate': extract_citations(thema_text),
                'teilaufgaben_anzahl': count_subtasks(thema_text),
                'volltext': thema_text.strip()
            })

    return aufgaben


def main():
    """Hauptprogramm"""
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / 'data' / 'mediendidaktik_alle_pruefungen.txt'
    output_file = base_dir / 'data' / 'aufgaben_parsed.json'

    print(f"📖 Lese: {input_file}")
    aufgaben = parse_aufgaben(str(input_file))

    print(f"✅ {len(aufgaben)} Aufgaben extrahiert")

    # Validierung
    print("\n🔍 Validierung:")
    print(f"   - Erwartete Aufgaben: 44")
    print(f"   - Gefundene Aufgaben: {len(aufgaben)}")

    # Statistiken
    all_themen = {}
    all_operators = {}

    for aufgabe in aufgaben:
        # Zähle Themen
        for kategorie, themen_liste in aufgabe['themen'].items():
            for thema in themen_liste:
                all_themen[thema] = all_themen.get(thema, 0) + 1

        # Zähle Operatoren
        for afb, ops in aufgabe['operatoren'].items():
            for op in ops:
                key = f"{afb}: {op}"
                all_operators[key] = all_operators.get(key, 0) + 1

    # Top 10 Themen
    top_themen = sorted(all_themen.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n📊 Top 10 Themen:")
    for thema, count in top_themen:
        print(f"   - {thema}: {count}x")

    # Speichern
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(aufgaben, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Gespeichert: {output_file}")
    print(f"   - Dateigröße: {output_file.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
