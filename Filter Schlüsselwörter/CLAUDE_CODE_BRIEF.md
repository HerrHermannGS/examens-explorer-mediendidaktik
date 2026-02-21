# Examens-Explorer Mediendidaktik – Projekt-Brief

## 🎯 Ziel
Erstelle eine **interaktive HTML-App** zur Durchsuchung von 44 Examensaufgaben (Mediendidaktik, 2015-2025).

---

## 📋 Anforderungen

### Funktionale Anforderungen
1. **Live-Suche**: Volltextsuche über alle Aufgaben
2. **Multi-Filter**: Kombinierbar nach Thema, Operator, Semester
3. **Aufgaben-Cards**: Klickbar, zeigen Tags + Zitate, Volltext ausklappbar
4. **Statistik-Dashboard**: Balkendiagramm "Top 10 Themen", AFB-Verteilung
5. **Offline-fähig**: Alles in EINER HTML-Datei, keine Server nötig
6. **Mobile-responsive**: Funktioniert auf Desktop + Tablet + Smartphone

### Daten-Anforderungen
**Input:** `mediendidaktik_alle_pruefungen.txt` (bereits vorhanden)

**Zu extrahieren:**
- Semester (z.B. "2022 Frühjahr")
- Thema-Nummer (1 oder 2)
- Operatoren mit AFB-Zuordnung
- Themen nach Kategorien (4 Boxen, siehe unten)
- Zitate (Text + Autor + Quelle)
- Teilaufgaben-Anzahl
- Volltext der Aufgabe

---

## 📊 Themen-Kategorien (aus "Wichtige_Themenbereiche.png")

### Grüne Box: Mediendidaktische Konzepte
SAMR, Puentedura, CTML, Mayer, Designeffekte, Digitale Lernaufgaben, ICAP, Chi, Wylie

### Lila Box: Lehr-Lerntheorien
Kognitivismus, Konstruktivismus, Konnektivismus, Instruktional Design, Problemorientierung, selbstreguliert, kollaborativ, kooperativ, Projektmethode, SCRUM, Kanban

### Blaue Box: Lernpsychologie
Cognitive Load Theory, CLT, Sweller, Drei-Speicher-Modell, Atkinson, Shiffrin, Motivation, Deci, Ryan, Assimilation, Akkommodation

### Gelbe Box: Spezifische Medien/Formate
Lernplattform, LMS, Moodle, Interactive Whiteboard, IWB, Tablet, Smartphone, BYOD, WebQuest, Tutorial, Erklärvideo, Flipped Classroom, E-Portfolio, Quiz, Abstimmungssystem, Gamification, AR, VR, Podcast, Audio, Visualisierung, Mindmap, Concept Map, Hypertext, Multimedia

---

## 🎨 Design-Vorgaben

### Farbschema
- **Primärfarbe:** #007bff (Blau)
- **Erfolg:** #28a745 (Grün) → AFB I
- **Warnung:** #ffc107 (Gelb) → AFB II  
- **Gefahr:** #dc3545 (Rot) → AFB III
- **Hintergrund:** #f8f9fa (Hellgrau)

### Schriftarten
- Überschriften: Arial Bold
- Fließtext: Arial Regular
- Monospace (Code/Zitate): Consolas

### Layout
- Max-Width: 1200px (zentriert)
- Card-Layout für Aufgaben (Shadow, Rounded Corners)
- Filter-Bar oben fixiert (Sticky)
- Responsive Breakpoints: 768px (Tablet), 480px (Mobile)

---

## 🔍 Operatoren mit AFB-Zuordnung

### AFB I (Reproduktion)
nennen, beschreiben, darstellen, wiedergeben, definieren, aufzeigen, benennen

### AFB II (Reorganisation/Transfer)
erklären, erläutern, zeigen Sie auf, begründen, charakterisieren, vergleichen, gegenüberstellen, analysieren, ableiten, einordnen

### AFB III (Reflexion/Problemlösung)
diskutieren, erörtern, beurteilen, bewerten, entwerfen, entwickeln, gestalten, konzipieren, skizzieren, überprüfen, prüfen, sich auseinandersetzen

---

## 🛠️ Tech-Stack

### Python (Parsing)
```python
import re
import json
from pathlib import Path

# Parse mediendidaktik_alle_pruefungen.txt
# Extrahiere: Semester, Themen, Operatoren, Zitate
# Output: aufgaben_parsed.json
```

### HTML/CSS/JavaScript
- **Framework:** Vanilla JS (keine Dependencies außer Chart.js für Diagramme)
- **Charts:** Chart.js von CDN
- **Icons:** Unicode-Emojis (keine Icon-Fonts nötig)
- **Storage:** LocalStorage für User-Preferences (Dark Mode, Fortschritt)

---

## 📁 Projekt-Struktur

```
examens-explorer/
├── data/
│   ├── mediendidaktik_alle_pruefungen.txt  (gegeben)
│   ├── Wichtige_Themenbereiche.png         (Referenz)
│   ├── Operatoren_fu_r_die_Pru_fung.png    (Referenz)
│   └── aufgaben_parsed.json                (generiert)
├── src/
│   └── parser.py                           (Python-Script)
├── dist/
│   └── examens_explorer.html               (finales Produkt)
├── README.md
└── requirements.txt                         (leer, da nur Stdlib)
```

---

## 🎯 Meilensteine

### Phase 1: Parsing
- [ ] Python-Script schreiben
- [ ] Alle 44 Aufgaben korrekt extrahieren
- [ ] JSON validieren (keine fehlenden Felder)

### Phase 2: HTML-Basis
- [ ] Grundstruktur (Header, Filter, Aufgabenliste)
- [ ] CSS-Styling (responsive, modern)
- [ ] JavaScript: Daten laden, Cards rendern

### Phase 3: Interaktivität
- [ ] Live-Suche implementieren
- [ ] Multi-Filter (Dropdowns + Checkboxes)
- [ ] Aufgaben ausklappen/einklappen

### Phase 4: Statistik
- [ ] Chart.js integrieren
- [ ] Top 10 Themen (Balkendiagramm)
- [ ] AFB-Verteilung (Pie-Chart)
- [ ] Semester-Timeline (optional)

### Phase 5: Polish
- [ ] Dark Mode Toggle
- [ ] Export-Funktion (gefilterte Liste → Markdown)
- [ ] LocalStorage (Fortschritt, Notizen)
- [ ] Mobile-Optimierung testen

---

## ✅ Akzeptanzkriterien

1. **Alle 44 Aufgaben korrekt geparst** (keine fehlenden Daten)
2. **Suche funktioniert live** (keine Verzögerung spürbar)
3. **Filter kombinierbar** (z.B. "CLT + AFB III + 2022")
4. **Eine HTML-Datei** (max. 5 MB, offline nutzbar)
5. **Mobile verwendbar** (keine horizontalen Scrollbalken auf Handy)
6. **Statistik-Charts korrekt** (Zahlen stimmen mit Realität überein)

---

## 🚫 Out-of-Scope (für v1.0)

- Backend/Datenbank
- User-Accounts / Cloud-Sync
- Kollaborative Notizen
- KI-generierte Musterlösungen
- PDF-Export

---

## 📚 Kontext-Files (im Projekt verfügbar)

1. `mediendidaktik_alle_pruefungen.txt` – Rohdaten (44 Aufgaben)
2. `Wichtige_Themenbereiche.png` – Themen-Taxonomie
3. `Operatoren_fu_r_die_Pru_fung.png` – AFB-Beispiele
4. `Alte_Themen_Didadktik_und_Erzieziehung_Examen.pdf` – Übersicht (optional)

---

## 🎓 Domänen-Kontext

**Zielgruppe:** Lehramtsstudierende, die sich auf Staatsexamen Medienpädagogik vorbereiten  
**Use-Case:** Gezielt nach Themen/Operatoren üben, Trends erkennen, Aufgaben vergleichen  
**Pain-Point:** Bisher: 10+ PDFs durchsuchen, manuell Tags setzen  
**Lösung:** Eine HTML-App, die alles strukturiert und durchsuchbar macht

---

## 💡 Nice-to-Have (Future Versions)

- [ ] Lernmodus: Zufällige Aufgabe + Timer
- [ ] Fortschritt-Tracking: "30/44 durchgearbeitet"
- [ ] Karteikarten-View: Flip-Animation
- [ ] Vergleichs-Modus: 2 Aufgaben nebeneinander
- [ ] Prognose-Panel: "Evergreens fällig?" (Statistik-basiert)

---

## 🤝 Kollaboration

**Chat-Claude (hier):**  
✅ Konzept entwickelt  
✅ Requirements definiert  
✅ Daten vorbereitet  

**Code-Claude (du):**  
🎯 Implementierung  
🎯 Testing  
🎯 Deployment  

---

## 📞 Kontakt bei Fragen

Falls während der Entwicklung Unklarheiten auftreten:
1. Check die Referenz-Bilder (`Wichtige_Themenbereiche.png`, `Operatoren_fu_r_die_Pru_fung.png`)
2. Validiere gegen die Original-TXT (Stichproben)
3. Im Zweifel: Conservative defaults (z.B. Thema nicht zuordnen statt falsch zuordnen)

---

**Let's build! 🚀**
