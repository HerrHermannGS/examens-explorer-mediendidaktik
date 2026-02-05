# 📋 TODO: Erweiterung für Medienerziehung

## 🎯 Ziel
Die Examens-Explorer App um den Bereich **Medienerziehung** erweitern, sodass beide Bereiche (Mediendidaktik + Medienerziehung) durchsuchbar sind.

---

## 📦 Phase 1: Daten-Vorbereitung

- [ ] Medienerziehung TXT-Datei beschaffen
  - [ ] Format: Analog zu `mediendidaktik_alle_pruefungen.txt`
  - [ ] Zeitraum: Idealerweise auch 2015-2025
  - [ ] Ablage: `data/medienerziehung_alle_pruefungen.txt`

- [ ] Themen-Kategorien für Medienerziehung definieren
  - [ ] Analog zu "Wichtige_Themenbereiche.png"
  - [ ] Kategorien wie:
    - Mediensozialisation
    - Jugendmedienschutz
    - Medienkompetenz
    - Medienethik
    - etc.

- [ ] Operatoren-Liste validieren
  - [ ] Prüfen ob AFB-Zuordnung identisch ist
  - [ ] Eventuell Medienerziehung-spezifische Operatoren ergänzen

---

## 🔧 Phase 2: Parser anpassen

- [ ] Parser erweitern für beide Bereiche
  - [ ] `src/parser.py` → neuer Parameter `--bereich [mediendidaktik|medienerziehung]`
  - [ ] Oder: Separate Parser `parser_mediendidaktik.py` + `parser_medienerziehung.py`
  - [ ] Output:
    - `data/mediendidaktik_parsed.json`
    - `data/medienerziehung_parsed.json`
    - `data/alle_aufgaben_parsed.json` (kombiniert)

- [ ] Themen-Kategorien anpassen
  - [ ] Neue Kategorien für Medienerziehung in Parser integrieren
  - [ ] Farbschema erweitern (aktuell 4 Farben, evtl. 6-8 für beide Bereiche)

- [ ] Aufgaben-Struktur erweitern
  - [ ] Neues Feld: `"bereich": "Mediendidaktik" | "Medienerziehung"`
  - [ ] Erlaubt später Filterung nach Bereich

---

## 🎨 Phase 3: UI anpassen

### Filter-Bar erweitern
- [ ] Neuer Dropdown: **Bereich-Filter**
  - [ ] Optionen: "Alle Bereiche", "Mediendidaktik", "Medienerziehung"
  - [ ] Platzierung: Links neben Semester-Filter

### Statistiken erweitern
- [ ] Neue Stat-Card: "Bereiche"
  - [ ] Zeigt Anzahl pro Bereich
  - [ ] z.B. "Mediendidaktik: 42 | Medienerziehung: 38"

- [ ] Charts anpassen
  - [ ] Top 10 Themen: Separate Charts oder kombiniert?
  - [ ] AFB-Verteilung: Pro Bereich oder gesamt?
  - [ ] Neuer Chart: Bereichs-Verteilung (Pie)

### Cards erweitern
- [ ] Bereich-Badge hinzufügen
  - [ ] Farbe: Blau für Mediendidaktik, Orange für Medienerziehung
  - [ ] Position: Neben Semester-Badge

### Themen-Tags
- [ ] Farbschema erweitern (aktuell 4 Kategorien)
  - [ ] Mediendidaktik: Grün, Lila, Blau, Gelb (wie bisher)
  - [ ] Medienerziehung: Rot, Pink, Türkis, Braun (neue Farben)
  - [ ] Oder: Bereich im Tooltip anzeigen

---

## 🔨 Phase 4: Build-Prozess

- [ ] `build.sh` anpassen
  - [ ] Parse beide Bereiche
  - [ ] Kombiniere JSONs
  - [ ] Baue Standalone HTML mit beiden Bereichen

- [ ] Dateigrößen prüfen
  - [ ] Aktuell: 92 KB (42 Aufgaben Mediendidaktik)
  - [ ] Erwartet: ~180 KB (80+ Aufgaben beide Bereiche)
  - [ ] Falls >200 KB: Optimierung überlegen (z.B. JSON minifizieren)

---

## 📊 Phase 5: Statistiken erweitern

- [ ] `src/statistik.py` erweitern
  - [ ] Separate Statistiken pro Bereich
  - [ ] Vergleichsstatistiken (Mediendidaktik vs. Medienerziehung)
  - [ ] z.B. "Welche Themen überschneiden sich?"

- [ ] Neue Analysen
  - [ ] Welche AFB-Verteilung pro Bereich?
  - [ ] Gibt es Semestermuster? (z.B. Medienerziehung immer im Herbst?)

---

## 🧪 Phase 6: Testing

- [ ] Test-Suite erweitern
  - [ ] Test: Beide Bereiche vorhanden
  - [ ] Test: Bereichs-Filter funktioniert
  - [ ] Test: Statistiken korrekt pro Bereich
  - [ ] Test: Dateigrößen im Rahmen

- [ ] Manual Testing
  - [ ] Mediendidaktik-Aufgaben anzeigen → funktioniert
  - [ ] Medienerziehung-Aufgaben anzeigen → funktioniert
  - [ ] Filter kombinieren (z.B. "Medienerziehung + 2022 + AFB III")
  - [ ] Charts zeigen korrekte Daten

---

## 📝 Phase 7: Dokumentation

- [ ] README aktualisieren
  - [ ] Erwähne beide Bereiche
  - [ ] Update Statistiken (80+ statt 42 Aufgaben)

- [ ] QUICK_START aktualisieren
  - [ ] Neue Beispiele mit Bereichs-Filter
  - [ ] Workflows für beide Bereiche

- [ ] PROJECT_SUMMARY aktualisieren
  - [ ] Version 2.0
  - [ ] Neue Features dokumentieren

---

## 🎯 Optionale Erweiterungen (Nice-to-Have)

- [ ] **Vergleichs-Modus**
  - [ ] Zwei Aufgaben nebeneinander anzeigen
  - [ ] z.B. "Gleiche Themen, aber Mediendidaktik vs. Medienerziehung"

- [ ] **Bereichs-Switcher**
  - [ ] Toggle: "Mediendidaktik ↔ Medienerziehung"
  - [ ] Behält Filter bei, wechselt nur Bereich

- [ ] **Export-Funktion**
  - [ ] Gefilterte Liste → Markdown
  - [ ] z.B. "Alle Medienerziehung AFB III → PDF"

- [ ] **Gemeinsame Themen hervorheben**
  - [ ] Zeige, welche Themen in BEIDEN Bereichen vorkommen
  - [ ] Hilft bei übergreifender Vorbereitung

---

## 🚀 Geschätzter Aufwand

| Phase | Aufwand | Priorität |
|-------|---------|-----------|
| 1. Daten-Vorbereitung | 1-2h | Hoch |
| 2. Parser anpassen | 2-3h | Hoch |
| 3. UI anpassen | 3-4h | Hoch |
| 4. Build-Prozess | 1h | Mittel |
| 5. Statistiken | 1-2h | Mittel |
| 6. Testing | 1h | Hoch |
| 7. Dokumentation | 1h | Mittel |
| **Gesamt** | **10-15h** | - |

Optional: +3-5h (je nach Features)

---

## 📌 Notizen

- **Kompatibilität**: Bestehende Mediendidaktik-Nutzer sollten weiterhin funktionieren
- **Rückwärtskompatibilität**: `mediendidaktik_parsed.json` als Fallback
- **URL-Parameter**: Optional `?bereich=medienerziehung` für Direktlink
- **LocalStorage**: Bereichs-Filter speichern für nächsten Besuch

---

## 🔗 Abhängigkeiten

**Benötigt VOR Start:**
1. Medienerziehung TXT-Datei (analog zu Mediendidaktik)
2. Themen-Kategorien-Liste für Medienerziehung
3. Eventuell Referenz-PDFs (wie "Wichtige_Themenbereiche.png")

**Kann parallel erledigt werden:**
- UI-Design für neue Farben
- Statistik-Konzept

---

**Status:** 📋 **Geplant für Version 2.0**

**Erstellt:** 2026-02-05
**Letztes Update:** 2026-02-05
