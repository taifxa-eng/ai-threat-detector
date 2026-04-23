const alertsPage = window.location.pathname === '/alerts';

if (alertsPage) {
    const alertsList = document.getElementById('alertsList');

    function renderAlerts(alerts) {
        alertsList.innerHTML = alerts.map(alert => `
            <div class="alert-card">
                <strong>${alert.title}</strong>
                <p>${alert.description}</p>
                <span>${new Date(alert.createdAt).toLocaleString()}</span>
            </div>
        `).join('');
    }

    async function refreshAlerts() {
        const response = await fetch('/api/alerts/live');
        if (!response.ok) return;
        const data = await response.json();
        renderAlerts(data.alerts);
    }

    refreshAlerts();
    setInterval(refreshAlerts, 6000);
}
