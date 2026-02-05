with open('build_with_operators.py', 'r') as f:
    content = f.read()

# Ersetze die fehlerhafte Regex-Zeile
content = content.replace(
    "const regex = new RegExp(`\\\\\\\\b${{op.text}}\\\\\\\\b`, 'gi');",
    "const regex = new RegExp(`\\\\b${{op.text}}\\\\b`, 'gi');"
)

with open('build_with_operators.py', 'w') as f:
    f.write(content)

print("✅ Regex gefixt: \\\\\\\\b -> \\\\b")
