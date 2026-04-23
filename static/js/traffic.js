const trafficPage = window.location.pathname === '/traffic';

if (trafficPage) {

    const suspiciousIps = document.getElementById('suspiciousIps');
    const attackCount = document.getElementById('attackCount');
    const suspiciousCount = document.getElementById('suspiciousCount');
    const trafficList = document.getElementById('trafficList');

    let isLoading = false;

    async function loadTraffic(){

        if(isLoading) return;
        isLoading = true;

        try{

            const res = await fetch('/api/traffic/summary');
            if(!res.ok) return;

            const data = await res.json();

            // 🔥 Suspicious IPs
            if(data.suspiciousIps && data.suspiciousIps.length > 0){
                suspiciousIps.innerHTML = data.suspiciousIps.map(item => `
                    <div style="background:#111;padding:10px;margin:8px 0;border-radius:8px">
                        <strong>${item.ip}</strong><br>
                        ${item.events} event(s)
                    </div>
                `).join('');
            } else {
                suspiciousIps.innerHTML = "<p>No suspicious IPs</p>";
            }

            // 🔥 Attack counters (نسخة نهائية قوية)
            let attacks = 0;
            let suspicious = 0;

            if (Array.isArray(data.attackBreakdown)) {
                data.attackBreakdown.forEach(i => {
                    attacks += Number(i.count || 0);
                });
            }

            if (Array.isArray(data.suspiciousIps)) {
                data.suspiciousIps.forEach(i => {
                    suspicious += Number(i.events || 0);
                });
            }

            attackCount.innerText = attacks.toLocaleString('en-US');
            suspiciousCount.innerText = suspicious.toLocaleString('en-US');

            // 🔥 Attack Breakdown list
            if(data.attackBreakdown && data.attackBreakdown.length > 0){
                trafficList.innerHTML = data.attackBreakdown.map(i => `
                    <div style="background:#111;padding:10px;margin:8px 0;border-radius:8px">
                        ${i.label} : ${Number(i.count || 0).toLocaleString('en-US')}
                    </div>
                `).join('');
            } else {
                trafficList.innerHTML = "<p>No attack data</p>";
            }

        } catch(e){
            console.log("traffic safe");
        }

        isLoading = false;
    }

    loadTraffic();

    // 🔥 تقليل الضغط (حل نهائي 429)
    setInterval(loadTraffic, 20000);
}