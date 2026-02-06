import json
import re
import os

def cleanup():
    data_path = 'data/aufgaben_parsed.json'
    detailed_path = 'data/operatoren_detailliert.json'
    
    if not os.path.exists(data_path) or not os.path.exists(detailed_path):
        print("Fehler: Dateien nicht gefunden.")
        return

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
    op_ref = {
        "nennen": "AFB I",
        "benennen": "AFB I",
        "beschreiben": "AFB I",
        "darstellen": "AFB I",
        "aufzählen": "AFB I",
        "wiedergeben": "AFB I",
        "aufzeigen": "AFB I",
        "zusammenfassen": "AFB I",
        "erläutern": "AFB II",
        "erklären": "AFB II",
        "vergleichen": "AFB II",
        "analysieren": "AFB II",
        "charakterisieren": "AFB II",
        "einordnen": "AFB II",
        "belegen": "AFB II",
        "herausarbeiten": "AFB II",
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
        "prüfen": "AFB III",
        "überprüfen": "AFB III",
        "setzen sie sich auseinander": "AFB III",
        "bewerten sie": "AFB III",
        "erläutern sie": "AFB II",
        "erklären sie": "AFB II",
        "nennen sie": "AFB I"
    }

    modified_count = 0
    
    for aufgabe in aufgaben:
        changed = False
        volltext = aufgabe['volltext']
        v_lower = volltext.lower()
        
        # --- 1. TEILAUFGABEN_ANZAHL ---
        matches = re.findall(r'(?m)^\s*(\d+)\.', volltext)
        if not matches:
            matches = re.findall(r'[ \n](\d+)\.', volltext)
            
        if matches:
            max_nr = max(int(m) for m in matches)
            if aufgabe['teilaufgaben_anzahl'] != max_nr:
                print(f"[{aufgabe['id']}] Teilaufgaben: {aufgabe['teilaufgaben_anzahl']} -> {max_nr}")
                aufgabe['teilaufgaben_anzahl'] = max_nr
                changed = True

        # --- 2. OPERATOREN ---
        new_operatoren_sets = {
            "AFB I": set(aufgabe['operatoren'].get("AFB I", [])),
            "AFB II": set(aufgabe['operatoren'].get("AFB II", [])),
            "AFB III": set(aufgabe['operatoren'].get("AFB III", []))
        }

        # Extrahiere Operatoren aus detailed data (falls vorhanden)
        d_entry = detailed_map.get(aufgabe['id'])
        if d_entry:
            for ta in d_entry['teilaufgaben']:
                for d_op in ta['operatoren']:
                    op_val = d_op['operator']
                    afb_val = d_op['afb']
                    level = f"AFB {afb_val}"
                    if level == "AFB 1": level = "AFB I"
                    if level == "AFB 2": level = "AFB II"
                    if level == "AFB 3": level = "AFB III"
                    
                    if level in new_operatoren_sets:
                        # Check if already present in any set (ignore case)
                        already_present = False
                        for l in new_operatoren_sets:
                            if any(op_val.lower() == existing.lower() for existing in new_operatoren_sets[l]):
                                already_present = True
                                break
                        
                        if not already_present:
                            new_operatoren_sets[level].add(op_val)
                            print(f"[{aufgabe['id']}] Operator aus Detailed-Daten ergänzt: {op_val} ({level})")
                            changed = True

        # Suche zusätzliche Operatoren im Volltext (die nicht in detailed-daten stehen)
        for op_key, default_level in op_ref.items():
            # Suche nach dem Operator im Volltext (Wortgrenzen beachten)
            if re.search(r'\b' + re.escape(op_key) + r'\b', v_lower):
                # Check if already present (ignore case)
                already_present = False
                for l in new_operatoren_sets:
                    if any(op_key.lower() == existing.lower() for existing in new_operatoren_sets[l]):
                        already_present = True
                        break
                
                if not already_present:
                    new_operatoren_sets[default_level].add(op_key.capitalize())
                    print(f"[{aufgabe['id']}] Operator aus Volltext ergänzt: {op_key} ({default_level})")
                    changed = True

        aufgabe['operatoren'] = {k: sorted(list(v)) for k, v in new_operatoren_sets.items()}

        # --- 3. ZITATE ---
        if 'zitate' in aufgabe:
            valid_zitate = []
            for zitat in aufgabe['zitate']:
                text = zitat['text']
                # Entferne Marker
                cleaned_search = text.replace('[...]', '').replace('...', '').replace('[', '').replace(']', '').strip()
                if not cleaned_search:
                    continue

                # Suche im Volltext
                # Nehme die ersten 20 Zeichen als Anker
                anchor = cleaned_search[:20]
                if anchor in volltext:
                    start_pos = volltext.find(anchor)
                    # Versuche das Ende zu finden (letzte 20 Zeichen)
                    end_anchor = cleaned_search[-20:]
                    end_pos = volltext.find(end_anchor, start_pos)
                    
                    if end_pos != -1:
                        # Extrahiere den Teil aus dem Volltext
                        full_version = volltext[start_pos:end_pos + len(end_anchor)].strip()
                        if full_version != zitat['text']:
                            print(f"[{aufgabe['id']}] Zitat im Volltext geheilt.")
                            zitat['text'] = full_version
                            changed = True
                        valid_zitate.append(zitat)
                    else:
                        # Wenn Ende nicht findbar aber Text sauber, behalten
                        if '[...]' not in text and '...' not in text:
                            valid_zitate.append(zitat)
                        else:
                            print(f"[{aufgabe['id']}] Zitat entfernt (unvollständig): {text[:20]}...")
                            changed = True
                else:
                    # Wenn gar nicht im Volltext, nur behalten wenn sauber
                    if '[...]' not in text and '...' not in text:
                        valid_zitate.append(zitat)
                    else:
                        print(f"[{aufgabe['id']}] Zitat entfernt (nicht im Volltext + unvollständig): {text[:20]}...")
                        changed = True
            aufgabe['zitate'] = valid_zitate

        if changed:
            modified_count += 1

    if modified_count > 0:
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(aufgaben, f, ensure_ascii=False, indent=2)
        print(f"\n✅ {modified_count} Aufgaben wurden aktualisiert.")

if __name__ == "__main__":
    cleanup()
