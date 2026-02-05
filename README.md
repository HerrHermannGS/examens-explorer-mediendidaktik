# Examens-Explorer Mediendidaktik

**Interaktive Web-App zur Durchsuchung von 42 Examensaufgaben (Mediendidaktik, 2015-2025)**

## 🚀 Features

- ✅ **Live-Volltextsuche** über alle Aufgaben
- ✅ **Multi-Filter** (Semester, AFB-Level, Themen)
- ✅ **Aufgaben-Cards** mit Tags, Zitaten und ausklappbarem Volltext
- ✅ **Statistik-Dashboard** (Top 10 Themen, AFB-Verteilung)
- ✅ **100% Offline-fähig** (Standalone HTML-Datei, 92 KB)
- ✅ **Dark Mode** mit LocalStorage-Persistenz
- ✅ **Mobile-responsive** (funktioniert auf allen Geräten)

## 📁 Projektstruktur

```
examens-explorer/
├── data/
│   ├── mediendidaktik_alle_pruefungen.txt  (Rohdaten)
│   ├── aufgaben_parsed.json                (Parsed JSON)
│   ├── Wichtige_Themenbereiche.png         (Referenz)
│   └── Operatoren_fu_r_die_Pru_fung.png    (Referenz)
├── src/
│   └── parser.py                           (Parser-Script)
├── dist/
│   ├── examens_explorer.html               (Reguläre Version)
│   └── examens_explorer_standalone.html    (Offline-Version mit Daten)
└── README.md
```

## 🎯 Verwendung

### Variante 1: Standalone (Empfohlen)
Öffne einfach `dist/examens_explorer_standalone.html` in einem Browser. Alle Daten sind eingebettet!

### Variante 2: Mit separater JSON-Datei
1. Kopiere `data/aufgaben_parsed.json` nach `dist/`
2. Öffne `dist/examens_explorer.html` (muss von einem lokalen Server geladen werden wegen CORS)

### Lokaler Server (für Entwicklung)
```bash
cd dist
python3 -m http.server 8000
# Öffne http://localhost:8000/examens_explorer.html
```

## 📊 Datenextraktion

Das Parser-Script extrahiert aus den Rohdaten:
- **Semester** (z.B. "2022 Frühjahr")
- **Thema-Nummer** (1 oder 2)
- **Operatoren** mit AFB-Zuordnung (I, II, III)
- **Themen** nach 4 Kategorien:
  - 🟢 Mediendidaktische Konzepte (SAMR, CTML, Designeffekte...)
  - 🟣 Lehr-Lerntheorien (Konstruktivismus, Instruktional Design...)
  - 🔵 Lernpsychologie (CLT, Motivation, Feedback...)
  - 🟡 Spezifische Medien (LMS, Tablets, AR/VR, Gamification...)
- **Zitate** (Text + Autor + Quelle)
- **Teilaufgaben-Anzahl**
- **Volltext** der Aufgabe

## 🔧 Parser neu ausführen

```bash
cd Lernanalyse
python3 src/parser.py
```

**Ausgabe:**
```
📖 Lese: data/mediendidaktik_alle_pruefungen.txt
✅ 42 Aufgaben extrahiert

🔍 Validierung:
   - Erwartete Aufgaben: 44
   - Gefundene Aufgaben: 42

📊 Top 10 Themen:
   - Lernplattform: 2x
   - Designeffekte: 2x
   - Feedback: 2x
   ...

💾 Gespeichert: data/aufgaben_parsed.json
   - Dateigröße: 69.4 KB
```

## 🎨 Farbschema

| Element | Farbe | Verwendung |
|---------|-------|------------|
| Primär | `#007bff` | Buttons, Links, Titel |
| AFB I | `#28a745` | Reproduktion (Grün) |
| AFB II | `#ffc107` | Transfer (Gelb) |
| AFB III | `#dc3545` | Reflexion (Rot) |
| Hintergrund | `#f8f9fa` | Light Mode |

## 📱 Mobile-Optimierung

- Responsive Breakpoints: 768px (Tablet), 480px (Mobile)
- Touch-freundliche Buttons und Filter
- Keine horizontalen Scrollbalken
- Optimierte Card-Layouts für kleine Screens

## 🌙 Dark Mode

- Toggle-Button (Floating) unten rechts
- Speichert Präferenz in LocalStorage
- Automatisches Laden beim nächsten Besuch

## ⚙️ Tech-Stack

- **Python 3**: Parser (Regex, JSON)
- **HTML5/CSS3**: Moderne Layouts (Flexbox, Grid)
- **Vanilla JavaScript**: Keine Frameworks (schneller Download)
- **Chart.js**: Visualisierungen (von CDN geladen)

## 🐛 Bekannte Einschränkungen

- **42 statt 44 Aufgaben**: 2 Aufgaben fehlen
  - Grund: 2025 Herbst existiert noch nicht (zukünftige Prüfung)
  - Alle verfügbaren Aufgaben (2015-2025 Frühjahr) sind vollständig erfasst ✅
- **OCR-Fehler behoben**: "@Thema Nr-" und "TThema" wurden manuell korrigiert
- **Zitat-Extraktion**: Funktioniert nur bei standardisierten Formaten (ca. 80% Erfolgsrate)

## 🚧 Zukünftige Verbesserungen (Nice-to-Have)

- [ ] Lernmodus: Zufällige Aufgabe + Timer
- [ ] Fortschritt-Tracking: "30/41 durchgearbeitet"
- [ ] Export-Funktion: Gefilterte Liste → Markdown
- [ ] Vergleichs-Modus: 2 Aufgaben nebeneinander
- [ ] Prognose-Panel: "Evergreens" (häufigste Themen)

## 📄 Lizenz

Dieses Projekt ist für Bildungszwecke erstellt. Die Prüfungsaufgaben unterliegen dem Copyright der jeweiligen Prüfungsbehörden.

## 🤝 Kontakt

Bei Fragen oder Verbesserungsvorschlägen: Öffne ein Issue oder Pull Request!

---

**Viel Erfolg bei der Examensvorbereitung! 📚✨**
