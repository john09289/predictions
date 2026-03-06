// DOME COSMOLOGY - VANILLA JS FRONTEND

// 1. Initial Data Load & AI Injection
document.addEventListener('DOMContentLoaded', () => {
    // Inject data into the hidden LD+JSON script tag for AI scrapers (Claude/Antigravity)
    const aiScriptNode = document.getElementById('dome-predictions-data');
    if (aiScriptNode) {
        aiScriptNode.textContent = JSON.stringify(PREDICTIONS, null, 2);
    }
    
    initScorecard();
    renderGrids();
    initNav();
    initCountdown();
});

// 2. Scorecard Calculation
function initScorecard() {
    const retrospective = PREDICTIONS.filter(p => p.status === 'confirmed').length;
    const falsified = PREDICTIONS.filter(p => p.status === 'falsified').length;
    const advance   = PREDICTIONS.filter(p => p.status === 'pending').length;
    
    const html = `
        <div class="score-hud"><span>${retrospective}</span> RETROSPECTIVE</div>
        <div class="score-hud"><span>${advance}</span> ADVANCE</div>
        <div class="score-hud" style="color:var(--status-falsified)"><span>${falsified}</span> FALSIFIED</div>
        <div class="score-hud"><span>${retrospective + advance}</span> TOTAL</div>
    `;
    
    document.getElementById('scorecard').innerHTML = html;
}

// 3. Grid Rendering
function createCardHTML(p) {
    let resultLine = '';
    if (p.status !== 'pending') {
        resultLine = `
        <div class="data-row" style="color:var(--status-${p.status}); margin-top:0.5rem; border-top:1px dashed #333; padding-top:0.5rem;">
            <span class="data-label">RESULT:</span>
            <span class="data-val">${p.result_value !== null ? p.result_value : ''} (${p.result_date ? p.result_date.split('T')[0] : ''})</span>
        </div>`;
    }

    return `
    <div class="pred-card">
        <div class="card-header">
            <span class="id-badge">${p.id}</span>
            <span class="status-badge ${p.status}">${p.status.toUpperCase()}</span>
        </div>
        <h3 class="card-title">${p.title}</h3>
        <p class="card-desc">${p.description}</p>
        
        <div class="data-row">
            <span class="data-label">TARGET DATE:</span>
            <span class="data-val" style="color:var(--acc-gold)">${p.test_date ? p.test_date.split('T')[0] : 'Ongoing'}</span>
        </div>
        <div class="data-row">
            <span class="data-label">PREDICTION:</span>
            <span class="data-val">${p.prediction.value !== null ? p.prediction.value : ''} ${p.prediction.unit || ''}</span>
        </div>
        
        ${resultLine}
        
        <div class="mech-box">
            <strong>MECHANISM:</strong> ${p.mechanism}
        </div>
        
        <div class="hash-foot">SHA256: ${p.sha256}</div>
    </div>
    `;
}

function renderGrids() {
    const allGrid = document.getElementById('all-grid');
    const confirmedGrid = document.getElementById('confirmed-grid');
    const pendingGrid = document.getElementById('pending-grid');
    const falsifiedGrid = document.getElementById('falsified-grid');
    const dashboardGrid = document.getElementById('dashboard-grid');

    let allHTML = '', confHTML = '', falsHTML = '', dashHTML = '', pendingHTML = '';

    PREDICTIONS.forEach(p => {
        const card = createCardHTML(p);
        allHTML += card;
        
        if (p.status === 'confirmed') confHTML += card;
        if (p.status === 'falsified') falsHTML += card;
        if (p.status === 'pending') pendingHTML += card;
        
        // Dashboard shows highest priority pending items (Eclipse 2026 + Core SAA mechanics)
        if (p.status === 'pending' && dashHTML.length < 15000) { 
            dashHTML += card; 
        }
    });

    if (allGrid) allGrid.innerHTML = allHTML;
    if (confirmedGrid) confirmedGrid.innerHTML = confHTML || '<div class="text-block">NO RECORDS</div>';
    if (pendingGrid) pendingGrid.innerHTML = pendingHTML || '<div class="text-block">NO RECORDS</div>';
    if (falsifiedGrid) falsifiedGrid.innerHTML = falsHTML || '<div class="text-block">NO RECORDS</div>';
    if (dashboardGrid) dashboardGrid.innerHTML = dashHTML;
}

// 4. Tab Navigation
function initNav() {
    const btns = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.view-section');

    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            btn.classList.add('active');
            const target = btn.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
        });
    });

    // Search bar functionality
    document.getElementById('search-bar').addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('#all-grid .pred-card');
        
        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            if (card.style) {
                if (text.includes(term)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    });
}

// 5. August 12 2026 Countdown Engine
function initCountdown() {
    const targetDate = new Date('2026-08-12T18:00:00Z').getTime();
    const display = document.getElementById('master-countdown');
    
    if(!display) return;

    setInterval(() => {
        const now = new Date().getTime();
        const distance = targetDate - now;
        
        if (distance < 0) {
            display.innerHTML = "ECLIPSE WINDOW ACTIVE";
            return;
        }
        
        const d = Math.floor(distance / (1000 * 60 * 60 * 24));
        const h = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((distance % (1000 * 60)) / 1000);
        
        display.innerHTML = `T-MINUS ${d.toString().padStart(3, '0')}:${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }, 1000);
}
