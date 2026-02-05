#!/usr/bin/env python3
"""
Statistik-Übersicht für Examens-Explorer
Zeigt detaillierte Auswertungen der geparsed Aufgaben
"""

import json
from collections import defaultdict, Counter
from pathlib import Path


def load_data():
    """Lade parsed JSON"""
    with open('data/aufgaben_parsed.json', 'r') as f:
        return json.load(f)


def print_header(title):
    """Schöner Header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def semester_overview(aufgaben):
    """Übersicht nach Semester"""
    print_header("📅 Semester-Übersicht")

    semester_count = Counter(a['semester'] for a in aufgaben)
    for semester in sorted(semester_count.keys()):
        count = semester_count[semester]
        bar = '█' * count
        print(f"  {semester:20s} {bar} ({count} Aufgaben)")

    print(f"\n  Gesamt: {len(aufgaben)} Aufgaben über {len(semester_count)} Semester")


def afb_overview(aufgaben):
    """AFB-Verteilung"""
    print_header("📊 AFB-Verteilung")

    afb_counts = defaultdict(int)
    for aufgabe in aufgaben:
        for afb, ops in aufgabe['operatoren'].items():
            afb_counts[afb] += len(ops)

    total = sum(afb_counts.values())
    for afb in ['AFB I', 'AFB II', 'AFB III']:
        count = afb_counts[afb]
        percentage = (count / total * 100) if total > 0 else 0
        bar_length = int(percentage / 2)
        bar = '█' * bar_length

        color = {'AFB I': '🟢', 'AFB II': '🟡', 'AFB III': '🔴'}[afb]
        print(f"  {color} {afb:10s} {bar:50s} {count:3d} ({percentage:4.1f}%)")


def themen_overview(aufgaben):
    """Top Themen"""
    print_header("🏆 Top 15 Themen")

    themen_count = Counter()
    for aufgabe in aufgaben:
        for kategorie, themen in aufgabe['themen'].items():
            for thema in themen:
                themen_count[thema] += 1

    for i, (thema, count) in enumerate(themen_count.most_common(15), 1):
        bar = '█' * count
        print(f"  {i:2d}. {thema:30s} {bar} ({count}x)")


def kategorie_overview(aufgaben):
    """Themen nach Kategorie"""
    print_header("📦 Themen nach Kategorie")

    kategorie_counts = defaultdict(int)
    for aufgabe in aufgaben:
        for kategorie, themen in aufgabe['themen'].items():
            kategorie_counts[kategorie] += len(themen)

    emoji_map = {
        'Mediendidaktische Konzepte': '🟢',
        'Lehr-Lerntheorien': '🟣',
        'Lernpsychologie': '🔵',
        'Spezifische Medien/Formate': '🟡'
    }

    total = sum(kategorie_counts.values())
    for kategorie, count in sorted(kategorie_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total * 100) if total > 0 else 0
        emoji = emoji_map.get(kategorie, '⚪')
        bar = '█' * int(percentage / 2)
        print(f"  {emoji} {kategorie:35s} {bar:30s} {count:3d} ({percentage:4.1f}%)")


def citation_overview(aufgaben):
    """Zitat-Statistik"""
    print_header("📝 Zitat-Statistik")

    with_citations = sum(1 for a in aufgaben if len(a['zitate']) > 0)
    total_citations = sum(len(a['zitate']) for a in aufgaben)

    print(f"  Aufgaben mit Zitaten: {with_citations}/{len(aufgaben)} ({with_citations/len(aufgaben)*100:.1f}%)")
    print(f"  Gesamt Zitate:        {total_citations}")
    print(f"  Ø Zitate pro Aufgabe: {total_citations/len(aufgaben):.2f}")

    # Top Autoren
    authors = Counter()
    for aufgabe in aufgaben:
        for zitat in aufgabe['zitate']:
            if zitat['author']:
                authors[zitat['author']] += 1

    if authors:
        print(f"\n  Top 5 zitierte Autoren:")
        for author, count in authors.most_common(5):
            print(f"    • {author}: {count}x")


def teilaufgaben_overview(aufgaben):
    """Teilaufgaben-Verteilung"""
    print_header("🔢 Teilaufgaben-Verteilung")

    teilaufgaben_count = Counter(a['teilaufgaben_anzahl'] for a in aufgaben)
    for anzahl in sorted(teilaufgaben_count.keys()):
        count = teilaufgaben_count[anzahl]
        bar = '█' * (count // 2)
        print(f"  {anzahl} Teilaufgaben: {bar:30s} ({count} Aufgaben)")


def main():
    """Hauptprogramm"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "EXAMENS-EXPLORER STATISTIKEN" + " " * 20 + "║")
    print("║" + " " * 15 + "Mediendidaktik 2015-2025" + " " * 19 + "║")
    print("╚" + "═" * 58 + "╝")

    aufgaben = load_data()

    semester_overview(aufgaben)
    afb_overview(aufgaben)
    themen_overview(aufgaben)
    kategorie_overview(aufgaben)
    citation_overview(aufgaben)
    teilaufgaben_overview(aufgaben)

    print("\n" + "=" * 60)
    print(f"✅ {len(aufgaben)} Aufgaben erfolgreich analysiert!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
