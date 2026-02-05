#!/bin/bash
# Deployment-Skript für Examens-Explorer

set -e

echo "🚀 Examens-Explorer Build & Deploy"
echo "===================================="
echo ""

# 1. Parse Daten
echo "📖 Schritt 1: Parse Examensaufgaben..."
python3 src/parser.py
echo "✅ Parsing abgeschlossen"
echo ""

# 2. Generiere Statistiken
echo "📊 Schritt 2: Erstelle Statistiken..."
python3 src/statistik.py > build_stats.txt
echo "✅ Statistiken gespeichert in build_stats.txt"
echo ""

# 3. Baue Standalone HTML
echo "🔨 Schritt 3: Baue Standalone HTML..."
python3 << 'PYTHON_EOF'
import json
from pathlib import Path

# Lade JSON
with open('data/aufgaben_parsed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lade HTML Template
with open('dist/examens_explorer.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Aktualisiere Anzahl
html = html.replace('44 Examensaufgaben', f'{len(data)} Examensaufgaben')

# Ersetze Placeholder
data_js = f'const AUFGABEN_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};'
html = html.replace('const AUFGABEN_DATA = /* PLACEHOLDER_DATA */;', data_js)

# Ersetze fetch() für offline
html = html.replace('fetch(\'aufgaben_parsed.json\')', '// fetch removed\nPromise.resolve({ json: () => Promise.resolve(AUFGABEN_DATA) })')

# Speichere
with open('dist/examens_explorer_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = Path('dist/examens_explorer_standalone.html').stat().st_size / 1024
print(f'✅ Standalone HTML: {size_kb:.1f} KB')
PYTHON_EOF
echo ""

# 4. Kopiere JSON auch in dist (für reguläre Version)
echo "📁 Schritt 4: Kopiere Dateien..."
cp data/aufgaben_parsed.json dist/
echo "✅ aufgaben_parsed.json → dist/"
echo ""

# 5. Validierung
echo "🔍 Schritt 5: Validiere Build..."
if [ ! -f "dist/examens_explorer_standalone.html" ]; then
    echo "❌ Fehler: Standalone HTML nicht gefunden!"
    exit 1
fi

if [ ! -f "dist/aufgaben_parsed.json" ]; then
    echo "❌ Fehler: JSON nicht gefunden!"
    exit 1
fi

echo "✅ Alle Dateien vorhanden"
echo ""

# 6. Zusammenfassung
echo "📦 Build-Zusammenfassung"
echo "========================"
echo "Dateien in dist/:"
ls -lh dist/ | grep -v "^total" | awk '{printf "  %-40s %8s\n", $9, $5}'
echo ""

echo "🎉 Deployment erfolgreich!"
echo ""
echo "Nächste Schritte:"
echo "  1. Öffne dist/examens_explorer_standalone.html im Browser"
echo "  2. Oder starte Server: cd dist && python3 -m http.server 8000"
echo ""
