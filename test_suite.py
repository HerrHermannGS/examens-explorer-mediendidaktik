#!/usr/bin/env python3
"""
Test-Suite für Examens-Explorer
Validiert alle Kernfunktionen
"""

import json
from pathlib import Path


def test_data_integrity():
    """Test 1: Daten-Integrität"""
    print("🧪 Test 1: Daten-Integrität")

    with open('data/aufgaben_parsed.json', 'r') as f:
        aufgaben = json.load(f)

    assert len(aufgaben) == 42, f"❌ Erwartete 42 Aufgaben, fand {len(aufgaben)}"

    # Prüfe Struktur
    required_fields = ['id', 'semester', 'thema_nr', 'operatoren', 'themen', 'zitate', 'teilaufgaben_anzahl', 'volltext']
    for i, aufgabe in enumerate(aufgaben):
        for field in required_fields:
            assert field in aufgabe, f"❌ Aufgabe {i} fehlt Feld '{field}'"

    print("  ✅ 42 Aufgaben mit korrekter Struktur")


def test_semester_coverage():
    """Test 2: Semester-Abdeckung"""
    print("\n🧪 Test 2: Semester-Abdeckung")

    with open('data/aufgaben_parsed.json', 'r') as f:
        aufgaben = json.load(f)

    semesters = set(a['semester'] for a in aufgaben)
    expected = 21  # 2015-2025 Frühjahr (kein 2025 Herbst)

    assert len(semesters) == expected, f"❌ Erwartete {expected} Semester, fand {len(semesters)}"
    print(f"  ✅ {len(semesters)} Semester korrekt abgedeckt")


def test_afb_distribution():
    """Test 3: AFB-Verteilung"""
    print("\n🧪 Test 3: AFB-Verteilung")

    with open('data/aufgaben_parsed.json', 'r') as f:
        aufgaben = json.load(f)

    afb_counts = {'AFB I': 0, 'AFB II': 0, 'AFB III': 0}
    for aufgabe in aufgaben:
        for afb, ops in aufgabe['operatoren'].items():
            afb_counts[afb] += len(ops)

    total = sum(afb_counts.values())
    assert total > 0, "❌ Keine Operatoren gefunden"

    # AFB II und III sollten dominieren
    assert afb_counts['AFB II'] + afb_counts['AFB III'] > afb_counts['AFB I'], \
        "❌ AFB I dominiert (unerwartetes Pattern)"

    print(f"  ✅ AFB-Verteilung: I={afb_counts['AFB I']}, II={afb_counts['AFB II']}, III={afb_counts['AFB III']}")


def test_themen_extraction():
    """Test 4: Themen-Extraktion"""
    print("\n🧪 Test 4: Themen-Extraktion")

    with open('data/aufgaben_parsed.json', 'r') as f:
        aufgaben = json.load(f)

    themen_count = 0
    for aufgabe in aufgaben:
        for kategorie, themen in aufgabe['themen'].items():
            themen_count += len(themen)

    assert themen_count > 0, "❌ Keine Themen extrahiert"
    print(f"  ✅ {themen_count} Themen-Zuordnungen gefunden")


def test_volltext_present():
    """Test 5: Volltext vorhanden"""
    print("\n🧪 Test 5: Volltext-Verfügbarkeit")

    with open('data/aufgaben_parsed.json', 'r') as f:
        aufgaben = json.load(f)

    for i, aufgabe in enumerate(aufgaben):
        assert len(aufgabe['volltext']) > 100, \
            f"❌ Aufgabe {i} ({aufgabe['id']}) hat zu kurzen Volltext"

    avg_length = sum(len(a['volltext']) for a in aufgaben) / len(aufgaben)
    print(f"  ✅ Alle Volltexte vorhanden (Ø {avg_length:.0f} Zeichen)")


def test_file_sizes():
    """Test 6: Dateigrößen"""
    print("\n🧪 Test 6: Dateigrößen")

    files_to_check = {
        'data/aufgaben_parsed.json': (50, 100),  # KB
        'dist/examens_explorer_standalone.html': (80, 150),
    }

    for filepath, (min_kb, max_kb) in files_to_check.items():
        path = Path(filepath)
        assert path.exists(), f"❌ Datei nicht gefunden: {filepath}"

        size_kb = path.stat().st_size / 1024
        assert min_kb <= size_kb <= max_kb, \
            f"❌ {filepath}: {size_kb:.1f} KB außerhalb Erwartung ({min_kb}-{max_kb} KB)"

        print(f"  ✅ {filepath}: {size_kb:.1f} KB")


def test_unique_ids():
    """Test 7: Eindeutige IDs"""
    print("\n🧪 Test 7: Eindeutige IDs")

    with open('data/aufgaben_parsed.json', 'r') as f:
        aufgaben = json.load(f)

    ids = [a['id'] for a in aufgaben]
    assert len(ids) == len(set(ids)), "❌ Doppelte IDs gefunden"
    print(f"  ✅ Alle {len(ids)} IDs eindeutig")


def test_html_structure():
    """Test 8: HTML-Struktur"""
    print("\n🧪 Test 8: HTML-Struktur")

    with open('dist/examens_explorer_standalone.html', 'r') as f:
        html = f.read()

    # Prüfe wichtige Elemente
    checks = [
        ('AUFGABEN_DATA', 'Eingebettete Daten'),
        ('Chart.js', 'Chart.js CDN'),
        ('searchInput', 'Suchfeld'),
        ('filterSemester', 'Semester-Filter'),
        ('darkModeToggle', 'Dark Mode Toggle'),
        ('cardsContainer', 'Cards Container'),
    ]

    for needle, name in checks:
        assert needle in html, f"❌ {name} nicht gefunden"
        print(f"  ✅ {name} vorhanden")


def main():
    """Hauptprogramm"""
    print("\n" + "="*60)
    print("  EXAMENS-EXPLORER TEST-SUITE")
    print("="*60)

    tests = [
        test_data_integrity,
        test_semester_coverage,
        test_afb_distribution,
        test_themen_extraction,
        test_volltext_present,
        test_file_sizes,
        test_unique_ids,
        test_html_structure,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n{e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ Unerwarteter Fehler in {test.__name__}: {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"  ERGEBNIS: {passed}/{len(tests)} Tests bestanden")
    if failed == 0:
        print("  🎉 ALLE TESTS ERFOLGREICH!")
    else:
        print(f"  ⚠️  {failed} Tests fehlgeschlagen")
    print("="*60 + "\n")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    exit(main())
