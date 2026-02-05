-- AppleScript zum automatischen Erstellen des GitHub Repos
tell application "Google Chrome"
	activate

	-- Öffne GitHub neue Repo Seite
	set repoURL to "https://github.com/new"
	open location repoURL
	delay 2

	-- JavaScript zum Ausfüllen des Formulars
	tell active tab of front window
		execute javascript "
			// Repository Name
			const nameInput = document.querySelector('input[name=\"repository[name]\"]');
			if (nameInput) nameInput.value = 'examens-explorer-mediendidaktik';

			// Description
			const descInput = document.querySelector('input[name=\"repository[description]\"]');
			if (descInput) descInput.value = 'Examens-Explorer für Mediendidaktik (42 Aufgaben, 2015-2025)';

			// Public Repository
			const publicRadio = document.querySelector('input[value=\"public\"]');
			if (publicRadio) publicRadio.click();

			// Warte kurz und submitte
			setTimeout(() => {
				const submitBtn = document.querySelector('button[type=\"submit\"]');
				if (submitBtn) {
					submitBtn.click();
					console.log('✅ Repository wird erstellt...');
				}
			}, 500);
		"
	end tell

	delay 3
	display dialog "✅ Repository erstellt! Drücke OK, dann pushe ich die Dateien." buttons {"OK"} default button 1
end tell
