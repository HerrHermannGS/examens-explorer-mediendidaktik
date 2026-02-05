#!/bin/bash
# GitHub Push Script für Examens-Explorer

echo "🚀 GitHub Upload - Examens-Explorer Mediendidaktik"
echo "=================================================="
echo ""

# Prüfe ob Git konfiguriert ist
if ! git config user.name > /dev/null 2>&1; then
    echo "⚙️  Konfiguriere Git..."
    git config user.name "HerrHermannGS"
    git config user.email "thomas@example.com"  # Bitte anpassen!
    echo "✅ Git konfiguriert"
fi

# Zeige aktuellen Status
echo ""
echo "📊 Repository Status:"
git log --oneline -3
echo ""
echo "📁 Dateien:"
git ls-files | wc -l | xargs echo "  Anzahl Dateien:"
echo ""

# Push zu GitHub
echo "🔄 Pushe zu GitHub..."
echo "Repository: https://github.com/HerrHermannGS/examens-explorer-mediendidaktik"
echo ""

# Versuche zu pushen
if git push -u origin main 2>&1; then
    echo ""
    echo "✅ Erfolgreich zu GitHub gepusht!"
    echo ""
    echo "🔗 Repository-URL:"
    echo "   https://github.com/HerrHermannGS/examens-explorer-mediendidaktik"
    echo ""
    echo "🌐 GitHub Pages (nach Aktivierung):"
    echo "   https://herrhermanngs.github.io/examens-explorer-mediendidaktik/dist/examens_explorer_standalone.html"
else
    echo ""
    echo "⚠️  Push fehlgeschlagen!"
    echo ""
    echo "Mögliche Gründe:"
    echo "1. Repository existiert noch nicht auf GitHub"
    echo "2. Keine Authentifizierung"
    echo ""
    echo "Nächste Schritte:"
    echo "1. Gehe zu: https://github.com/new"
    echo "2. Repository Name: examens-explorer-mediendidaktik"
    echo "3. Description: Interaktive Web-App für 42 Examensaufgaben Mediendidaktik (2015-2025)"
    echo "4. Public Repository"
    echo "5. KEIN README, .gitignore oder License hinzufügen (haben wir schon)"
    echo "6. Klicke 'Create repository'"
    echo ""
    echo "Danach erneut ausführen: ./github_push.sh"
fi
