const dashboardPage = window.location.pathname === '/dashboard';

if (dashboardPage) {

    let trafficChart;
    let attackChart;
    let isLoading = false;

    function generateColors(count){
        return ["#ff3b3b","#ffb100","#2ecc71","#00d4ff","#8a4fff"].slice(0,count);
    }

    // 🔥 تنسيق الأرقام (إنجليزي + مختصر)
    function formatNumber(num){

        if(num >= 1000000){
            return (num / 1000000).toFixed(1) + "M";
        }

        if(num >= 1000){
            return (num / 1000).toFixed(1) + "K";
        }

        return num.toString();
    }

    async function load(){

        if (isLoading) return;
        isLoading = true;

        try {

            const [summary, alerts, traffic] = await Promise.all([
                fetch('/api/dashboard/summary').then(r=>r.json()),
                fetch('/api/dashboard/alerts').then(r=>r.json()),
                fetch('/api/traffic/summary').then(r=>r.json())
            ]);

            // 🔢 أرقام
            document.getElementById('totalTraffic').innerText =
                formatNumber(summary.totalTraffic || 0);

            document.getElementById('threatCount').innerText =
                formatNumber(summary.threatCount || 0);

            document.getElementById('systemStatus').innerText =
                summary.status || "OK";

            // 🚨 Alerts
            const feed = document.getElementById("alertsFeed");
            feed.innerHTML = "";

            (alerts.alerts || []).forEach(a=>{
                const result = a.result || "SAFE";

                let color = "#2ecc71";
                if (result === "MALICIOUS") color = "#ff3b3b";
                if (result === "SUSPICIOUS") color = "#ffb100";

                feed.innerHTML += `
                <div style="background:#111;padding:10px;margin:10px;border-radius:10px;border-left:4px solid ${color}">
                    <b>${a.behavior}</b><br>
                    ${a.ip} | ${result} | Score: ${a.score}
                </div>`;
            });

            // 📈 Line Chart (تم تعديل الوقت + الأرقام فقط)
            if (traffic.history && document.getElementById("trafficChart")) {

                trafficChart?.destroy();

                trafficChart = new Chart(document.getElementById("trafficChart"), {
                    type: 'line',
                    data: {
                        labels: traffic.history.map(i =>
                            new Date(i.timestamp).toLocaleTimeString('en-US')
                        ),
                        datasets: [{
                            data: traffic.history.map(i => i.bytes || 0),
                            borderColor: '#00d4ff',
                            fill: true
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                ticks: {
                                    callback: function(value){
                                        return value.toLocaleString('en-US');
                                    }
                                }
                            }
                        }
                    }
                });
            }

            // 🍩 Donut (بدون تغيير)
            if (traffic.attackBreakdown && document.getElementById("attackMixChart")) {

                attackChart?.destroy();

                attackChart = new Chart(document.getElementById("attackMixChart"), {
                    type: 'doughnut',
                    data: {
                        labels: traffic.attackBreakdown.map(i => i.label),
                        datasets: [{
                            data: traffic.attackBreakdown.map(i => i.count || 0),
                            backgroundColor: generateColors(traffic.attackBreakdown.length)
                        }]
                    }
                });
            }

        } catch(e){
            console.log("safe dashboard");
        }

        isLoading = false;
    }

    load();
    setInterval(load, 30000);
}