// ✅ Kopiere diesen Code in die Chrome DevTools Console (F12 oder Cmd+Option+J)
// Dann drücke Enter!

console.log('🚀 Starte automatische Repository-Erstellung...');

// Repository Name
const nameInput = document.querySelector('input[name="repository[name]"]') || 
                  document.querySelector('#repository_name');
if (nameInput) {
    nameInput.value = 'examens-explorer-mediendidaktik';
    nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    console.log('✅ Name gesetzt');
}

// Description
const descInput = document.querySelector('input[name="repository[description]"]') || 
                  document.querySelector('#repository_description');
if (descInput) {
    descInput.value = 'Examens-Explorer für Mediendidaktik (42 Aufgaben, 2015-2025)';
    descInput.dispatchEvent(new Event('input', { bubbles: true }));
    console.log('✅ Description gesetzt');
}

// Public Repository
const publicRadio = document.querySelector('input[value="public"]') || 
                    document.querySelector('#repository_visibility_public');
if (publicRadio && !publicRadio.checked) {
    publicRadio.click();
    console.log('✅ Public selected');
}

console.log('\n🎯 Formular ausgefüllt!');
console.log('📝 Prüfe die Werte und klicke dann auf "Create repository"');
console.log('   ODER führe aus: document.querySelector("button[type=submit]").click()');
