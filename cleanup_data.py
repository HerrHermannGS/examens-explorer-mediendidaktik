import json
import re
import os

def cleanup():
    data_path = 'data/aufgaben_parsed.json'
    detailed_path = 'data/operatoren_detailliert.json'
    
    with open(data_path, 'r', encoding='utf-8') as f:
        aufgaben = json.load(f)
        
    with open(detailed_path, 'r', encoding='utf-8') as f:
        detailed = json.load(f)
        
    # Build a map from detailed data for easy lookup
    detailed_map = {}
    for entry in detailed:
        key = f"{entry['termin']}_{entry['jahr']}_T{entry['thema_nr']}"
        detailed_map[key] = entry
        
    # Reference list of common operators and their typical AFB levels
    # This is a bit flexible as levels can vary slightly depending on context
    op_ref = {
        "nennen": "AFB I",
        "benennen": "AFB I",
        "beschreiben": "AFB I",
        "darstellen": "AFB I",
        "aufzählen": "AFB I",
        "wiedergeben": "AFB I",
        "aufzeigen": "AFB I",
        "erläutern": "AFB II",
        "erklären": "AFB II",
        "vergleichen": "AFB II",
        "analysieren": "AFB II",
        "charakterisieren": "AFB II",
        "einordnen": "AFB II",
        "belegen": "AFB II",
        "zeigen sie auf": "AFB II",
        "stellen sie dar": "AFB II",
        "skizzieren": "AFB II",
        "bewerten": "AFB III",
        "beurteilen": "AFB III",
        "stellung nehmen": "AFB III",
        "diskutieren": "AFB III",
        "erörtern": "AFB III",
        "entwerfen": "AFB III",
        "konzipieren": "AFB III",
        "entwickeln": "AFB III",
        "gestalten": "AFB III",
        "reflektieren": "AFB III",
        "begründen": "AFB III",
        "setzen sie sich auseinander": "AFB III"
    }

    modified_count = 0
    
    for aufgabe in aufgaben:
        changed = False
        volltext = aufgabe['volltext']
        
        # 1. Teilaufgaben Anzahl korrigieren
        # Suche nach "1.", "2.", "3." etc. am Anfang einer Zeile oder nach Newline
        matches = re.findall(r'(?m)^\s*(\d+)\.', volltext)
        if not matches:
            # Manchmal sind sie nicht am Anfang der Zeile
            matches = re.findall(r'\s(\d+)\.', volltext)
            
        if matches:
            max_nr = max(int(m) for m in matches)
            if aufgabe['teilaufgaben_anzahl'] != max_nr:
                print(f"[{aufgabe['id']}] Teilaufgaben: {aufgabe['teilaufgaben_anzahl']} -> {max_nr}")
                aufgabe['teilaufgaben_anzahl'] = max_nr
                changed = True

        # 2. Operatoren prüfen
        # Wir sammeln alle Operatoren aus dem volltext
        found_ops = set()
        v_lower = volltext.lower()
        
        # Spezielle Phrasen zuerst
        phrases = ["stellen sie dar", "zeigen sie auf", "setzen sie sich auseinander", "stellung nehmen"]
        for p in phrases:
            if p in v_lower:
                found_ops.add(p)
                v_lower = v_lower.replace(p, " ") # Verhindere Doppelzählung von "darstellen" etc.

        # Einzelwörter
        words = re.findall(r'\b\w+\b', v_lower)
        for w in words:
            if w in op_ref and w not in ["sie", "sich"]: # "sie" und "sich" sind keine Operatoren
                found_ops.add(w)

        # Abgleich mit existing operatoren
        new_operatoren = {
            "AFB I": set(aufgabe['operatoren'].get("AFB I", [])),
            "AFB II": set(aufgabe['operatoren'].get("AFB II", [])),
            "AFB III": set(aufgabe['operatoren'].get("AFB III", []))
        }
        
        # Ergänze fehlende aus found_ops
        for op in found_ops:
            # Check if already present (case insensitive)
            present = False
            for level in new_operatoren:
                if any(op.lower() == existing.lower() for existing in new_operatoren[level]):
                    present = True
                    break
            
            if not present:
                # Welches AFB?
                level = op_ref.get(op.lower(), "AFB II") # Default II if unknown
                
                # Check detailed map for better level accuracy
                d_entry = detailed_map.get(aufgabe['id'])
                if d_entry:
                    for ta in d_entry['teilaufgaben']:
                        for d_op in ta['operatoren']:
                            if d_op['operator'].lower() == op.lower():
                                level = f"AFB {d_op['afb']}"
                                if level == "AFB 1": level = "AFB I"
                                if level == "AFB 2": level = "AFB II"
                                if level == "AFB 3": level = "AFB III"
                
                new_operatoren[level].add(op.capitalize())
                print(f"[{aufgabe['id']}] Operator ergänzt: {op} -> {level}")
                changed = True

        # Zurückverwandeln in Listen
        aufgabe['operatoren'] = {k: sorted(list(v)) for k, v in new_operatoren.items()}

        # 3. Zitate korrigieren
        if 'zitate' in aufgabe:
            valid_zitate = []
            for zitat in aufgabe['zitate']:
                text = zitat['text']
                # Wenn abgeschnitten ODER in volltext findbar
                cleaned_text = text.replace('[...]', '').replace('...', '').strip()
                # Versuche den vollständigen Satz im Volltext zu finden
                # Wir suchen nach den ersten 20 Zeichen des Zitats im Volltext
                snippet = cleaned_text[:30]
                if snippet in volltext:
                    # Finde den ganzen Satz oder den Abschnitt im Volltext
                    # Da Zitate oft am Anfang stehen, schauen wir ob wir den Text dort finden
                    pos = volltext.find(snippet)
                    if pos != -1:
                        # Wir nehmen den Teil aus dem Volltext bis zum Ende des Satzes oder Anführungszeichen
                        # Einfacher: Da wir keine neuen Zitate hinzufügen sollen, 
                        # versuchen wir nur das bestehende zu heilen.
                        # Wenn das Zitat im Volltext ist, nehmen wir den Teil der so aussieht wie das Zitat.
                        
                        # Suche nach dem Ende-Snippet
                        end_snippet = cleaned_text[-30:]
                        end_pos = volltext.find(end_snippet, pos)
                        if end_pos != -1:
                            full_version = volltext[pos:end_pos + len(end_snippet)].strip()
                            if full_version != zitat['text']:
                                print(f"[{aufgabe['id']}] Zitat vervollständigt: {zitat['text'][:30]}...")
                                zitat['text'] = full_version
                                changed = True
                        valid_zitate.append(zitat)
                    else:
                        # Wenn nicht im Volltext, behalten wir es wenn es nicht zu kaputt ist
                        if '[...]' not in text:
                            valid_zitate.append(zitat)
                        else:
                            print(f"[{aufgabe['id']}] Zitat entfernt (abgeschnitten/nicht heilbar): {text[:30]}...")
                            changed = True
                else:
                    if '[...]' not in text:
                         valid_zitate.append(zitat)
                    else:
                        print(f"[{aufgabe['id']}] Zitat entfernt (nicht im Volltext): {text[:30]}...")
                        changed = True
            aufgabe['zitate'] = valid_zitate

        if changed:
            modified_count += 1

    if modified_count > 0:
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(aufgaben, f, ensure_ascii=False, indent=2)
        print(f"\n✅ {modified_count} Aufgaben wurden aktualisiert.")
    else:
        print("\n✨ Keine Änderungen notwendig.")

if __name__ == "__main__":
    cleanup()
