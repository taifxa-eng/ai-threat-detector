async function loadReports() {
    try {
        const response = await fetch("/reports/data");
        const alerts = await response.json();

        const attacksTable = document.getElementById("attacksTable");
        const networkTable = document.getElementById("networkTable");

        attacksTable.innerHTML = "";
        networkTable.innerHTML = "";

        alerts.forEach(alert => {

            const date = alert.createdAt ? new Date(alert.createdAt).toLocaleString() : "-";

            const row = `
<tr>
    <td>${alert.id}</td>
    <td>${alert.ip}</td>
    <td>${alert.behavior}</td>
    <td>${alert.packets}</td>
    <td>${alert.result}</td>
    <td>${alert.score}</td>
    <td>${date}</td>
</tr>
`;

            if (alert.score >= 70) {
                attacksTable.innerHTML += row;
            } else {
                networkTable.innerHTML += row;
            }
        });

    } catch (err) {
        console.error("Reports error:", err);
    }
}

document.addEventListener("DOMContentLoaded", loadReports);