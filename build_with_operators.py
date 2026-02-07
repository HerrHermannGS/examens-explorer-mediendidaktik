#!/usr/bin/env python3
"""
Build-Skript für Examens-Explorer mit Operator-Highlighting
Aktualisiert die HTML-Datei mit detaillierten Operatoren-Daten
"""

import json
from pathlib import Path

def build_standalone_html_with_operators():
    """Erstellt Standalone-HTML mit Operator-Highlighting-Feature"""

    base_dir = Path(__file__).parent

    # Lade Aufgaben und Operatoren
    with open(base_dir / 'data' / 'aufgaben_parsed.json', 'r', encoding='utf-8') as f:
        aufgaben = json.load(f)

    with open(base_dir / 'data' / 'operatoren_detailliert.json', 'r', encoding='utf-8') as f:
        operatoren_detailliert = json.load(f)

    # Baue Lookup-Table: {termin}_{jahr}_T{thema_nr} -> operatoren
    operatoren_map = {}
    for op_data in operatoren_detailliert:
        key = f"{op_data['termin']}_{op_data['jahr']}_T{op_data['thema_nr']}"
        operatoren_map[key] = op_data

    print(f"✅ {len(aufgaben)} Aufgaben geladen")
    print(f"✅ {len(operatoren_map)} Operatoren-Definitionen geladen")

    # HTML-Template
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Examens-Explorer Mediendidaktik</title>
    <style>
        :root {{
            --primary: #007bff;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --bg-light: #f8f9fa;
            --dark: #212529;
            --border-radius: 8px;
            --shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, sans-serif;
            background: var(--bg-light);
            color: var(--dark);
            line-height: 1.6;
        }}

        body.dark-mode {{
            --bg-light: #1a1a1a;
            --dark: #e0e0e0;
            background: #1a1a1a;
            color: #e0e0e0;
        }}

        body.dark-mode .card {{
            background: #2d2d2d;
            border-color: #444;
        }}

        body.dark-mode .filter-bar {{
            background: #2d2d2d;
            border-color: #444;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: var(--primary);
            color: white;
            padding: 20px 0;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }}

        header h1 {{
            text-align: center;
            font-size: 2rem;
        }}

        header p {{
            text-align: center;
            opacity: 0.9;
            margin-top: 5px;
        }}

        .filter-bar {{
            position: sticky;
            top: 0;
            background: white;
            padding: 15px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 20px;
            z-index: 100;
        }}

        .filter-group {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-group input,
        .filter-group select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            flex: 1;
            min-width: 200px;
        }}

        .filter-group button {{
            padding: 8px 16px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }}

        .filter-group button:hover {{
            background: #0056b3;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            text-align: center;
        }}

        body.dark-mode .stat-card {{
            background: #2d2d2d;
        }}

        .stat-card h3 {{
            color: var(--primary);
            font-size: 2.5rem;
            margin-bottom: 5px;
        }}

        .stat-card p {{
            color: #666;
            font-size: 0.9rem;
        }}

        body.dark-mode .stat-card p {{
            color: #999;
        }}

        .card {{
            background: white;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }}

        .card-header {{
            margin-bottom: 15px;
        }}

        .card-title {{
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 10px;
        }}
        .card-stichpunkte {{
            font-size: 0.9rem;
            color: #666;
            font-style: italic;
            margin-bottom: 12px;
            padding: 8px 12px;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        body.dark-mode .card-stichpunkte {{
            background: #2d2d2d;
            color: #999;
        }}


        .card-meta {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 600;
            color: white;
        }}

        .badge.semester {{
            background: #6c757d;
        }}

        .badge.afb-i {{
            background: var(--success);
        }}

        .badge.afb-ii {{
            background: var(--warning);
            color: #333;
        }}

        .badge.afb-iii {{
            background: var(--danger);
        }}

        .tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }}

        .tag {{
            background: #e9ecef;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .tag:hover {{
            background: #dee2e6;
            transform: translateY(-1px);
        }}

        .tag.kategorie-1 {{ background: #d4edda; color: #155724; }}
        .tag.kategorie-2 {{ background: #e2d9f3; color: #4a148c; }}
        .tag.kategorie-3 {{ background: #cfe2ff; color: #084298; }}
        .tag.kategorie-4 {{ background: #fff3cd; color: #664d03; }}

        /* Dark Mode Tags (Tailwind-like colors) */
        body.dark-mode .tag.kategorie-1 {{ background: rgba(20, 83, 45, 0.4); color: #86efac; border: 1px solid rgba(134, 239, 172, 0.2); }}
        body.dark-mode .tag.kategorie-2 {{ background: rgba(88, 28, 135, 0.4); color: #d8b4fe; border: 1px solid rgba(216, 180, 254, 0.2); }}
        body.dark-mode .tag.kategorie-3 {{ background: rgba(30, 58, 138, 0.4); color: #93c5fd; border: 1px solid rgba(147, 197, 253, 0.2); }}
        body.dark-mode .tag.kategorie-4 {{ background: rgba(113, 63, 18, 0.4); color: #fde047; border: 1px solid rgba(253, 224, 71, 0.2); }}

        .citation {{
            background: #f8f9fa;
            border-left: 4px solid var(--primary);
            padding: 10px 15px;
            margin-bottom: 10px;
            font-style: italic;
        }}

        .citation-author {{
            display: block;
            margin-top: 5px;
            font-weight: bold;
            font-style: normal;
            color: #666;
        }}

        .toggle-btn {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
            transition: background 0.3s;
        }}

        .toggle-btn:hover {{
            background: #0056b3;
        }}

        .operator-toggle-btn {{
            background: #6c757d;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            margin: 10px 5px 10px 0;
            transition: all 0.3s;
        }}

        .operator-toggle-btn:hover {{
            background: #5a6268;
        }}

        .operator-toggle-btn.active {{
            background: var(--primary);
            box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
        }}

        .volltext {{
            display: none;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            white-space: pre-wrap;
            line-height: 1.8;
        }}

        .volltext.show {{
            display: block;
        }}

        /* Operator-Highlighting */
        .operator-highlight {{
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: 600;
            cursor: help;
            transition: all 0.2s;
        }}

        .operator-highlight:hover {{
            transform: scale(1.05);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}

        .operator-highlight.afb-1 {{
            background: rgba(40, 167, 69, 0.3);
            color: #155724;
        }}

        .operator-highlight.afb-2 {{
            background: rgba(255, 193, 7, 0.3);
            color: #664d03;
        }}

        .operator-highlight.afb-3 {{
            background: rgba(220, 53, 69, 0.3);
            color: #721c24;
        }}

        .dark-mode-toggle {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary);
            color: white;
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            box-shadow: var(--shadow);
            z-index: 1000;
        }}

        .dark-mode-toggle:hover {{
            background: #0056b3;
        }}

        @media (max-width: 768px) {{
            .filter-group {{
                flex-direction: column;
            }}

            .filter-group input,
            .filter-group select {{
                min-width: 100%;
            }}
        }}

        /* Favorites & Filter Toggle */
        .fav-btn {{
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.5rem;
            color: #ccc;
            transition: all 0.2s;
            padding: 0 5px;
        }}

        .fav-btn.active {{
            color: #ffc107;
            transform: scale(1.1);
        }}

        .fav-btn:hover {{
            transform: scale(1.2);
            color: #ffd54f;
        }}

        .filter-toggle {{
            background: white !important;
            color: var(--dark) !important;
            border: 1px solid #ddd !important;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .filter-toggle.active {{
            background: var(--warning) !important;
            color: #333 !important;
            border-color: var(--warning) !important;
            font-weight: bold;
        }}

        /* Notes Editor */
        .note-toggle-btn {{
            background: #6c757d;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }}

        .note-toggle-btn:hover {{
            background: #5a6268;
        }}

        .note-toggle-btn.has-note {{
            background: #17a2b8;
        }}

        .note-container {{
            display: none;
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px dashed #ccc;
        }}

        .note-container.show {{
            display: block;
        }}

        .note-textarea {{
            width: 100%;
            min-height: 120px;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            line-height: 1.5;
        }}

        .note-textarea:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }}

        .note-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .note-label {{
            font-weight: 600;
            color: #495057;
            font-size: 0.9rem;
        }}

        .note-saved {{
            color: #28a745;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.3s;
        }}

        body.dark-mode .note-container {{
            background: #2a2a2a;
            border-color: #444;
        }}

        body.dark-mode .note-textarea {{
            background: #1a1a1a;
            color: #e0e0e0;
            border-color: #444;
        }}

        body.dark-mode .note-label {{
            color: #ccc;
        }}

        /* AI Prompt Button */
        .prompt-btn {{
            background: #4f46e5;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}

        .prompt-btn:hover {{
            background: #4338ca;
            transform: translateY(-1px);
        }}

        .prompt-btn:active {{
            transform: translateY(0);
        }}

        .prompt-btn.copied {{
            background: #059669 !important;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📚 Examens-Explorer Mediendidaktik</h1>
            <p>Durchsuche 40 Examensaufgaben (2015-2025) mit Operator-Highlighting 🔍</p>
        </div>
    </header>

    <div class="container">
        <div class="filter-bar">
            <div class="filter-group">
                <input type="text" id="searchInput" placeholder="🔎 Volltextsuche..." />
                <select id="semesterFilter">
                    <option value="">Alle Semester</option>
                </select>
                <select id="afbFilter">
                    <option value="">Alle AFB-Level</option>
                    <option value="AFB I">AFB I (Reproduktion)</option>
                    <option value="AFB II">AFB II (Transfer)</option>
                    <option value="AFB III">AFB III (Reflexion)</option>
                </select>
                <select id="kategorieFilter">
                    <option value="">Alle Kategorien</option>
                    <option value="Mediendidaktische Konzepte">Mediendidaktische Konzepte</option>
                    <option value="Lehr-Lerntheorien">Lehr-Lerntheorien</option>
                    <option value="Lernpsychologie">Lernpsychologie</option>
                    <option value="Spezifische Medien/Formate">Spezifische Medien/Formate</option>
                </select>
                <select id="themaFilter">
                    <option value="">Alle Themen/Schlüsselwörter</option>
                </select>
                <button id="favFilterBtn" class="filter-toggle">⭐ Merkliste</button>
                <button id="resetBtn">🔄 Zurücksetzen</button>
            </div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3 id="totalCount">0</h3>
                <p>Aufgaben gesamt</p>
            </div>
            <div class="stat-card">
                <h3 id="visibleCount">0</h3>
                <p>Angezeigte Aufgaben</p>
            </div>
            <div class="stat-card">
                <h3 id="semesterCount">0</h3>
                <p>Semester (2015-2025)</p>
            </div>
        </div>

        <div id="results"></div>
    </div>

    <button class="dark-mode-toggle" onclick="toggleDarkMode()">🌙</button>

    <script>
        // Eingebettete Daten
        const aufgaben = {json.dumps(aufgaben, ensure_ascii=False, indent=2)};
        const operatorenDetailliert = {json.dumps(operatoren_detailliert, ensure_ascii=False, indent=2)};

        // Operatoren-Mapping erstellen
        const operatorenMap = {{}};
        operatorenDetailliert.forEach(op => {{
            const key = `${{op.termin}}_${{op.jahr}}_T${{op.thema_nr}}`;
            operatorenMap[key] = op;
        }});

        // Favoriten laden
        let favorites = new Set(JSON.parse(localStorage.getItem('favorites') || '[]'));
        let showFavoritesOnly = false;

        // Notizen laden
        let notes = JSON.parse(localStorage.getItem('notes') || '{{}}');

        // Debounce-Funktion für Auto-Save
        function debounce(func, wait) {{
            let timeout;
            return function executedFunction(...args) {{
                const later = () => {{
                    clearTimeout(timeout);
                    func.apply(this, args);
                }};
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            }};
        }}

        let filteredAufgaben = [...aufgaben];

        // Dark Mode
        function toggleDarkMode() {{
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
            document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
        }}

        // Dark Mode aus LocalStorage laden
        if (localStorage.getItem('darkMode') === 'true') {{
            toggleDarkMode();
        }}

        // Initialisierung
        document.addEventListener('DOMContentLoaded', () => {{
            populateFilters();
            renderResults();
            updateStats();
            attachEventListeners();
        }});

        function populateFilters() {{
            const semesters = [...new Set(aufgaben.map(a => a.semester))].sort();
            const semesterFilter = document.getElementById('semesterFilter');

            semesters.forEach(sem => {{
                const option = document.createElement('option');
                option.value = sem;
                option.textContent = sem;
                semesterFilter.appendChild(option);
            }});

            populateThemaFilter();
        }}

        function populateThemaFilter(selectedKategorie) {{
            const themaFilter = document.getElementById('themaFilter');
            const currentValue = themaFilter.value;
            themaFilter.innerHTML = '<option value="">Alle Themen/Schlüsselwörter</option>';

            const themenSet = new Set();
            aufgaben.forEach(aufgabe => {{
                Object.entries(aufgabe.themen).forEach(([kategorie, themen]) => {{
                    if (!selectedKategorie || kategorie === selectedKategorie) {{
                        themen.forEach(t => themenSet.add(t));
                    }}
                }});
            }});

            [...themenSet].sort((a, b) => a.localeCompare(b, 'de')).forEach(thema => {{
                const option = document.createElement('option');
                option.value = thema;
                option.textContent = thema;
                themaFilter.appendChild(option);
            }});

            if ([...themenSet].includes(currentValue)) {{
                themaFilter.value = currentValue;
            }}
        }}

        function attachEventListeners() {{
            document.getElementById('searchInput').addEventListener('input', filterResults);
            document.getElementById('semesterFilter').addEventListener('change', filterResults);
            document.getElementById('afbFilter').addEventListener('change', filterResults);
            document.getElementById('kategorieFilter').addEventListener('change', function() {{
                populateThemaFilter(this.value);
                filterResults();
            }});
            document.getElementById('themaFilter').addEventListener('change', filterResults);
            
            document.getElementById('favFilterBtn').addEventListener('click', function() {{
                showFavoritesOnly = !showFavoritesOnly;
                this.classList.toggle('active');
                filterResults();
            }});

            document.getElementById('resetBtn').addEventListener('click', resetFilters);
        }}

        function toggleFavorite(id) {{
            if (favorites.has(id)) {{
                favorites.delete(id);
            }} else {{
                favorites.add(id);
            }}
            localStorage.setItem('favorites', JSON.stringify([...favorites]));
            
            // Button Update (visuell)
            const btn = document.querySelector(`.fav-btn[data-card-id="${{id}}"]`);
            if (btn) {{
                btn.classList.toggle('active');
                btn.textContent = favorites.has(id) ? '⭐' : '☆';
            }}

            // Wenn Filter aktiv, Liste aktualisieren
            if (showFavoritesOnly) {{
                filterResults();
            }}
        }}

        function saveNote(id, text) {{
            notes[id] = text;
            localStorage.setItem('notes', JSON.stringify(notes));
            
            // Visuelles Feedback
            const savedIndicator = document.querySelector(`#note-container-${{id}} .note-saved`);
            if (savedIndicator) {{
                savedIndicator.style.opacity = '1';
                setTimeout(() => savedIndicator.style.opacity = '0', 1500);
            }}

            // Button-Style aktualisieren (hat Notiz?)
            const btn = document.querySelector(`.note-toggle-btn[data-card-id="${{id}}"]`);
            if (btn) {{
                if (text.trim()) {{
                    btn.classList.add('has-note');
                }} else {{
                    btn.classList.remove('has-note');
                }}
            }}
        }}

        function copyKIPrompt(id) {{
            const aufgabe = aufgaben.find(a => a.id === id);
            if (!aufgabe) return;

            // Operatoren Text bauen
            let opText = "";
            Object.entries(aufgabe.operatoren).forEach(([afb, ops]) => {{
                if (ops.length > 0) {{
                    opText += `- ${{afb}}: ${{ops.join(', ')}}\\n`;
                }}
            }});

            const prompt = `Du bist ein fachdidaktischer Experte für Mediendidaktik. Basierend auf der folgenden Examensaufgabe aus dem Jahr ${{aufgabe.semester}}, erstelle mir eine strukturierte Antwort oder eine detaillierte Gliederung.

Aufgabe:
"${{aufgabe.volltext}}"

Berücksichtige dabei unbedingt die folgenden Operatoren und deren Anforderungsbereiche:
${{opText}}

Die Antwort soll wissenschaftlich fundiert und präzise auf die bayerischen Staatsexamens-Anforderungen zugeschnitten sein.`;

            navigator.clipboard.writeText(prompt).then(() => {{
                const btn = document.querySelector(`.prompt-btn[data-card-id="${{id}}"]`);
                if (btn) {{
                    const originalText = btn.innerHTML;
                    btn.innerHTML = "✨ Prompt kopiert!";
                    btn.classList.add('copied');
                    setTimeout(() => {{
                        btn.innerHTML = originalText;
                        btn.classList.remove('copied');
                    }}, 2000);
                }}
            }});
        }}

        function filterResults() {{
            const search = document.getElementById('searchInput').value.toLowerCase();
            const semester = document.getElementById('semesterFilter').value;
            const afb = document.getElementById('afbFilter').value;
            const kategorie = document.getElementById('kategorieFilter').value;
            const thema = document.getElementById('themaFilter').value;

            filteredAufgaben = aufgaben.filter(aufgabe => {{
                const alleThemen = Object.values(aufgabe.themen).flat().map(t => t.toLowerCase());

                const matchSearch = !search ||
                    aufgabe.volltext.toLowerCase().includes(search) ||
                    aufgabe.semester.toLowerCase().includes(search) ||
                    (aufgabe.stichpunkte && aufgabe.stichpunkte.toLowerCase().includes(search)) ||
                    alleThemen.some(t => t.includes(search)) ||
                    (aufgabe.titel && aufgabe.titel.toLowerCase().includes(search));

                const matchSemester = !semester || aufgabe.semester === semester;

                const matchAFB = !afb ||
                    (aufgabe.operatoren[afb] && aufgabe.operatoren[afb].length > 0);

                const matchKategorie = !kategorie ||
                    (aufgabe.themen[kategorie] && aufgabe.themen[kategorie].length > 0);

                const matchThema = !thema ||
                    Object.values(aufgabe.themen).some(themen => themen.includes(thema));

                const matchFav = !showFavoritesOnly || favorites.has(aufgabe.id);

                return matchSearch && matchSemester && matchAFB && matchKategorie && matchThema && matchFav;
            }});

            renderResults();
            updateStats();
        }}

        function resetFilters() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('semesterFilter').value = '';
            document.getElementById('afbFilter').value = '';
            document.getElementById('kategorieFilter').value = '';
            document.getElementById('themaFilter').value = '';
            populateThemaFilter();

            showFavoritesOnly = false;
            document.getElementById('favFilterBtn').classList.remove('active');

            filterResults();
        }}

        function renderResults() {{
            const resultsDiv = document.getElementById('results');

            if (filteredAufgaben.length === 0) {{
                resultsDiv.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">Keine Aufgaben gefunden</p>';
                return;
            }}

            resultsDiv.innerHTML = filteredAufgaben.map(aufgabe => renderCard(aufgabe)).join('');

            // Event Listeners für Toggle-Buttons
            document.querySelectorAll('.toggle-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const cardId = this.dataset.cardId;
                    const volltext = document.getElementById('volltext-' + cardId);
                    volltext.classList.toggle('show');
                    this.textContent = volltext.classList.contains('show')
                        ? '▲ Volltext verbergen'
                        : '▼ Volltext anzeigen';
                }});
            }});

            // Event Listeners für Operator-Toggle-Buttons
            document.querySelectorAll('.operator-toggle-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const cardId = this.dataset.cardId;
                    toggleOperatorHighlighting(cardId);
                    this.classList.toggle('active');
                    this.textContent = this.classList.contains('active')
                        ? '✓ Operatoren markiert'
                        : '🔍 Operatoren markieren';
                }});
            }});

            // Event Listeners für Favoriten-Buttons
            document.querySelectorAll('.fav-btn').forEach(btn => {{
                btn.addEventListener('click', function(e) {{
                    e.stopPropagation(); // Verhindert Bubbling
                    const cardId = this.dataset.cardId;
                    toggleFavorite(cardId);
                }});
            }});

            // Event Listeners für Notizen-Toggle
            document.querySelectorAll('.note-toggle-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const cardId = this.dataset.cardId;
                    const container = document.getElementById('note-container-' + cardId);
                    if (container) {{
                        container.classList.toggle('show');
                        this.textContent = container.classList.contains('show')
                            ? '📝 Notizen schließen'
                            : (notes[cardId]?.trim() ? '📝 Notizen (✓)' : '📝 Notizen');
                    }}
                }});
            }});

            // Event Listeners für Notizen-Textareas (Auto-Save)
            document.querySelectorAll('.note-textarea').forEach(textarea => {{
                const debouncedSave = debounce(function() {{
                    const cardId = this.dataset.cardId;
                    saveNote(cardId, this.value);
                }}, 500);
                
                textarea.addEventListener('input', debouncedSave);
            }});

            // Event Listeners für AI Prompt
            document.querySelectorAll('.prompt-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const cardId = this.dataset.cardId;
                    copyKIPrompt(cardId);
                }});
            }});
        }}

        function renderCard(aufgabe) {{
            const kategorieTags = [];
            const kategorieMap = {{
                'Mediendidaktische Konzepte': 1,
                'Lehr-Lerntheorien': 2,
                'Lernpsychologie': 3,
                'Spezifische Medien/Formate': 4
            }};

            Object.entries(aufgabe.themen).forEach(([kategorie, themen]) => {{
                themen.forEach(thema => {{
                    const kategorieNum = kategorieMap[kategorie] || 1;
                    kategorieTags.push(`<span class="tag kategorie-${{kategorieNum}}" title="${{kategorie}}">${{thema}}</span>`);
                }});
            }});

            const operatorBadges = [];
            Object.entries(aufgabe.operatoren).forEach(([afb, ops]) => {{
                if (ops.length > 0) {{
                    const afbClass = afb.replace(' ', '-').toLowerCase();
                    operatorBadges.push(`<span class="badge ${{afbClass}}">${{afb}}: ${{ops.join(', ')}}</span>`);
                }}
            }});

            const citations = aufgabe.zitate.map(zitat => `
                <div class="citation">
                    "${{zitat.text.substring(0, 150)}}${{zitat.text.length > 150 ? '...' : ''}}"
                    <span class="citation-author">— ${{zitat.source}}</span>
                </div>
            `).join('');
            
            const isFav = favorites.has(aufgabe.id);
            const noteText = notes[aufgabe.id] || '';
            const hasNote = noteText.trim().length > 0;

            return `
                <div class="card">
                    <div class="card-header">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div class="card-title">${{aufgabe.semester}} – ${{aufgabe.titel || `Thema ${{aufgabe.thema_nr}}`}}</div>
                            <button class="fav-btn ${{isFav ? 'active' : ''}}" data-card-id="${{aufgabe.id}}" title="Aufgabe merken">${{isFav ? '⭐' : '☆'}}</button>
                        </div>
                        ${{aufgabe.stichpunkte ? `
                            <div class="card-stichpunkte">
                                📌 ${{aufgabe.stichpunkte}}
                            </div>
                        ` : ""}}

                        <div class="card-meta">
                            <span class="badge semester">${{aufgabe.semester}}</span>
                            <span class="badge">${{aufgabe.teilaufgaben_anzahl}} Teilaufgaben</span>
                        </div>
                    </div>

                    ${{operatorBadges.length > 0 ? `
                        <div class="tags">
                            ${{operatorBadges.join(' ')}}
                        </div>
                    ` : ''}}

                    ${{kategorieTags.length > 0 ? `
                        <div class="tags">
                            ${{kategorieTags.join(' ')}}
                        </div>
                    ` : ''}}

                    ${{citations}}

                    <button class="toggle-btn" data-card-id="${{aufgabe.id}}">▼ Volltext anzeigen</button>
                    <button class="operator-toggle-btn" data-card-id="${{aufgabe.id}}">🔍 Operatoren markieren</button>
                    <button class="note-toggle-btn ${{hasNote ? 'has-note' : ''}}" data-card-id="${{aufgabe.id}}">${{hasNote ? '📝 Notizen (✓)' : '📝 Notizen'}}</button>
                    <button class="prompt-btn" data-card-id="${{aufgabe.id}}">🤖 Prompt kopieren</button>
                    
                    <div class="volltext" id="volltext-${{aufgabe.id}}">${{aufgabe.volltext}}</div>
                    
                    <div class="note-container" id="note-container-${{aufgabe.id}}">
                        <div class="note-header">
                            <span class="note-label">Deine Gliederung / Notizen:</span>
                            <span class="note-saved">✓ Gespeichert</span>
                        </div>
                        <textarea class="note-textarea" placeholder="Hier Gliederung oder Ideen festhalten..." data-card-id="${{aufgabe.id}}">${{noteText}}</textarea>
                    </div>
                </div>
            `;
        }}

        function toggleOperatorHighlighting(cardId) {{
            console.log('🔍 Highlighting aufgerufen für:', cardId);
            const volltextDiv = document.getElementById('volltext-' + cardId);

            // Wenn bereits highlighted, zurücksetzen
            if (volltextDiv.dataset.highlighted === 'true') {{
                const aufgabe = aufgaben.find(a => a.id === cardId);
                volltextDiv.innerHTML = aufgabe.volltext;
                volltextDiv.dataset.highlighted = 'false';
                return;
            }}

            // Finde die passenden Operator-Definitionen
            const [termin, jahr, thema] = cardId.split('_');
            const thema_nr = parseInt(thema.replace('T', ''));
            const key = `${{termin}}_${{jahr}}_T${{thema_nr}}`;

            const opData = operatorenMap[key];
            console.log('📋 Operator-Daten:', opData ? 'gefunden' : 'FEHLT', 'für Key:', key);
            if (!opData) {{
                console.warn('Keine Operator-Daten gefunden für:', cardId);
                return;
            }}

            // Sammle alle Operatoren mit AFB-Level
            const operatoren = [];
            opData.teilaufgaben.forEach(teilaufgabe => {{
                teilaufgabe.operatoren.forEach(op => {{
                    operatoren.push({{
                        text: op.operator,
                        afb: op.afb,
                        bezug: op.bezug,
                        textform: op.textform
                    }});
                }});
            }});

            // Highlighte Operatoren im Text
            let highlightedText = volltextDiv.innerHTML;

            // Sortiere nach Länge (längste zuerst), um Überlappungen zu vermeiden
            operatoren.sort((a, b) => b.text.length - a.text.length);
            console.log('📝 Operatoren zum Highlighten:', operatoren.length, operatoren.map(o => o.text));

            operatoren.forEach(op => {{
                // Escape Sonderzeichen für Regex
                const escapedText = op.text.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
                // Verwende flexible Regex ohne \\b für mehrteilige Operatoren
                const regex = new RegExp(`(${{escapedText}})`, 'gi');
                const replacement = `<span class="operator-highlight afb-${{op.afb}}" title="AFB ${{op.afb}}: ${{op.textform}} | ${{op.bezug}}">$1</span>`;
                highlightedText = highlightedText.replace(regex, replacement);
            }});

            volltextDiv.innerHTML = highlightedText;
            console.log('✅ Highlighting abgeschlossen');
            volltextDiv.dataset.highlighted = 'true';
        }}

        function updateStats() {{
            document.getElementById('totalCount').textContent = aufgaben.length;
            document.getElementById('visibleCount').textContent = filteredAufgaben.length;
            const semesters = new Set(aufgaben.map(a => a.semester));
            document.getElementById('semesterCount').textContent = semesters.size;
        }}
    </script>
</body>
</html>"""

    # Speichere HTML
    output_file = base_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    file_size = output_file.stat().st_size / 1024
    print(f"\n💾 Gespeichert: {output_file}")
    print(f"   - Dateigröße: {file_size:.1f} KB")
    print(f"\n✨ Neue Features:")
    print(f"   - 🔍 Operator-Highlighting mit AFB-Farben")
    print(f"   - 📝 Tooltips mit Bezug und Textform")
    print(f"   - 🎯 Klickbare Toggle-Buttons pro Aufgabe")
    print(f"\n🎨 Farbschema:")
    print(f"   - AFB I (Reproduktion): Grün")
    print(f"   - AFB II (Transfer): Gelb")
    print(f"   - AFB III (Reflexion): Rot")

if __name__ == '__main__':
    build_standalone_html_with_operators()
