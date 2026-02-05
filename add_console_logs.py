with open('build_with_operators.py', 'r') as f:
    content = f.read()

# Füge Console-Logs hinzu
replacements = [
    # Bei Funktionsaufruf
    (
        "function toggleOperatorHighlighting(cardId) {{",
        "function toggleOperatorHighlighting(cardId) {{\n            console.log('🔍 Highlighting aufgerufen für:', cardId);"
    ),
    # Bei Operator-Daten gefunden
    (
        "const opData = operatorenMap[key];",
        "const opData = operatorenMap[key];\n            console.log('📋 Operator-Daten:', opData ? 'gefunden' : 'FEHLT', 'für Key:', key);"
    ),
    # Bei Operatoren sammeln
    (
        "operatoren.sort((a, b) => b.text.length - a.text.length);",
        "operatoren.sort((a, b) => b.text.length - a.text.length);\n            console.log('📝 Operatoren zum Highlighten:', operatoren.length, operatoren.map(o => o.text));"
    ),
    # Nach Highlighting
    (
        "volltextDiv.dataset.highlighted = 'true';",
        "console.log('✅ Highlighting abgeschlossen');\n            volltextDiv.dataset.highlighted = 'true';"
    )
]

for old, new in replacements:
    content = content.replace(old, new)

with open('build_with_operators.py', 'w') as f:
    f.write(content)

print("✅ Console-Logs hinzugefügt!")
