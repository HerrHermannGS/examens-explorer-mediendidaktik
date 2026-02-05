#!/usr/bin/env python3
from pypdf import PdfReader

reader = PdfReader('data/Alte Themen Didadktik und Erzieziehung Examen.pdf')
print(f'Seiten: {len(reader.pages)}')

# Extrahiere erste 5 Seiten
for i in range(min(5, len(reader.pages))):
    print('\n' + '='*60)
    print(f'SEITE {i+1}')
    print('='*60)
    text = reader.pages[i].extract_text()
    print(text)
