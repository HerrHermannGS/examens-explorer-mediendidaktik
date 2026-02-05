#!/usr/bin/env python3
"""
Debug-Version mit Console-Logging für Operator-Highlighting
"""

import json
from pathlib import Path

# Kopiere nur den relevanten Teil - die toggleOperatorHighlighting Funktion
debug_function = """
        function toggleOperatorHighlighting(cardId) {
            console.log('🔍 toggleOperatorHighlighting aufgerufen für:', cardId);

            const volltextDiv = document.getElementById('volltext-' + cardId);
            console.log('📄 Volltext-Div gefunden:', volltextDiv ? 'JA' : 'NEIN');

            // Wenn bereits highlighted, zurücksetzen
            if (volltextDiv.dataset.highlighted === 'true') {
                console.log('🔄 Bereits highlighted, setze zurück');
                const aufgabe = aufgaben.find(a => a.id === cardId);
                volltextDiv.innerHTML = aufgabe.volltext;
                volltextDiv.dataset.highlighted = 'false';
                return;
            }

            // Finde die passenden Operator-Definitionen
            const [jahr, termin, thema] = cardId.split('_');
            const thema_nr = parseInt(thema.replace('T', ''));
            const key = `${jahr}_${termin}_T${thema_nr}`;

            console.log('🔑 Key für Operator-Lookup:', key);

            const opData = operatorenMap[key];
            if (!opData) {
                console.error('❌ Keine Operator-Daten gefunden für:', key);
                console.log('📋 Verfügbare Keys:', Object.keys(operatorenMap).slice(0, 5));
                return;
            }

            console.log('✅ Operator-Daten gefunden:', opData);

            // Sammle alle Operatoren mit AFB-Level
            const operatoren = [];
            opData.teilaufgaben.forEach(teilaufgabe => {
                teilaufgabe.operatoren.forEach(op => {
                    operatoren.push({
                        text: op.operator,
                        afb: op.afb,
                        bezug: op.bezug,
                        textform: op.textform
                    });
                });
            });

            console.log('📝 Gefundene Operatoren:', operatoren.length);
            console.log('📝 Operatoren-Details:', operatoren);

            // Highlighte Operatoren im Text
            let highlightedText = volltextDiv.innerHTML;
            console.log('📄 Original-Text (erste 200 Zeichen):', highlightedText.substring(0, 200));

            // Sortiere nach Länge (längste zuerst), um Überlappungen zu vermeiden
            operatoren.sort((a, b) => b.text.length - a.text.length);

            let replacementCount = 0;
            operatoren.forEach(op => {
                // WICHTIG: Nur 2 Backslashes für \\b (Wortgrenze)
                const regex = new RegExp(`\\\\b${op.text}\\\\b`, 'gi');
                const replacement = `<span class="operator-highlight afb-${op.afb}" title="AFB ${op.afb}: ${op.textform} | ${op.bezug}">$&</span>`;

                const beforeLength = highlightedText.length;
                highlightedText = highlightedText.replace(regex, replacement);
                const afterLength = highlightedText.length;

                if (afterLength > beforeLength) {
                    replacementCount++;
                    console.log(`✅ Operator "${op.text}" gefunden und markiert (AFB ${op.afb})`);
                } else {
                    console.log(`⚠️  Operator "${op.text}" NICHT gefunden im Text`);
                }
            });

            console.log(`🎨 Insgesamt ${replacementCount} Operatoren markiert`);
            console.log('📄 Highlighted-Text (erste 200 Zeichen):', highlightedText.substring(0, 200));

            volltextDiv.innerHTML = highlightedText;
            volltextDiv.dataset.highlighted = 'true';
            console.log('✅ Highlighting abgeschlossen!');
        }
"""

print("Debug-Funktion erstellt!")
print("\nErsetze diese Funktion in build_with_operators.py:")
print("Suche nach: 'function toggleOperatorHighlighting'")
print("\nOder führe das komplette Rebuild aus:")

# Lese Original
base_dir = Path(__file__).parent
with open(base_dir / 'build_with_operators.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Finde und ersetze die Funktion
import re
pattern = r'function toggleOperatorHighlighting\(cardId\).*?volltextDiv\.dataset\.highlighted = \'true\';'
match = re.search(pattern, content, re.DOTALL)

if match:
    # Extrahiere Einrückung
    lines_before = content[:match.start()].split('\n')
    indent = len(lines_before[-1]) - len(lines_before[-1].lstrip())

    # Füge Einrückung zur Debug-Funktion hinzu
    debug_lines = debug_function.strip().split('\n')
    indented_debug = '\n'.join(' ' * indent + line if line.strip() else '' for line in debug_lines)

    # Ersetze
    new_content = content[:match.start()] + indented_debug + '\n' + ' ' * indent + '}' + content[match.end():]

    # Speichere
    with open(base_dir / 'build_with_operators_debug.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ Debug-Version erstellt: build_with_operators_debug.py")
    print("\nJetzt ausführen:")
    print("  python3 build_with_operators_debug.py")
else:
    print("❌ Funktion nicht gefunden!")
