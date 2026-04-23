const settingsPage = window.location.pathname === '/settings';

if (settingsPage) {
    const form = document.getElementById('passwordForm');
    const message = document.getElementById('settingsMessage');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const response = await fetch('/api/settings/password', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();
        message.textContent = result.message || (result.success ? 'Password updated.' : 'Unable to update password.');
        message.style.color = result.success ? '#4cff99' : '#ff6b91';
    });
}
