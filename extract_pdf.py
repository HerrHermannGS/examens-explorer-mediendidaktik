#!/usr/bin/env python3
"""
PDF Extractor für Didaktik Prüfungen
Extrahiert Text aus der sauberen PDF-Datei
"""

from pypdf import PdfReader
from pathlib import Path

def extract_pdf_to_txt(pdf_path: str, output_path: str):
    """Extrahiert Text aus PDF und speichert in TXT-Datei"""

    print(f"📖 Lese PDF: {pdf_path}")
    reader = PdfReader(pdf_path)

    print(f"   - Seiten: {len(reader.pages)}")

    all_text = []

    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if text.strip():
            # Bereinige den Text: Entferne einzelne Leerzeilen zwischen Wörtern
            # aber behalte echte Absätze
            lines = text.split('\n')
            cleaned_lines = []

            for line in lines:
                stripped = line.strip()
                if stripped:
                    cleaned_lines.append(stripped)

            # Füge Zeilen zu einem zusammenhängenden Text zusammen
            page_text = ' '.join(cleaned_lines)

            # Ersetze mehrfache Leerzeichen durch ein einzelnes
            page_text = ' '.join(page_text.split())

            all_text.append(f"\n{'='*80}\nSEITE {i}\n{'='*80}\n")
            all_text.append(page_text)
            print(f"   ✅ Seite {i} extrahiert ({len(page_text)} Zeichen)")

    # Speichern
    full_text = '\n'.join(all_text)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"\n💾 Gespeichert: {output_path}")
    print(f"   - Gesamtgröße: {len(full_text):,} Zeichen")
    print(f"   - Dateigröße: {Path(output_path).stat().st_size / 1024:.1f} KB")

    return full_text


if __name__ == '__main__':
    base_dir = Path(__file__).parent
    pdf_file = base_dir / 'Didaktik Prüfungen Alle Aufgaben final.pdf'
    output_file = base_dir / 'data' / 'mediendidaktik_alle_pruefungen.txt'

    extract_pdf_to_txt(str(pdf_file), str(output_file))
