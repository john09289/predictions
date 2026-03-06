// DOME COSMOLOGY - VANILLA JS FRONTEND

document.addEventListener('DOMContentLoaded', () => {
    // Inject master data into the hidden LD+JSON script tag for AI scrapers 
    const aiScriptNode = document.getElementById('dome-predictions-data');
    if (aiScriptNode) {
        const fullPayload = {
            metadata: { version: "V49.2", updated: new Date().toISOString() },
            master_predictions: PREDICTIONS,
            weekly_active_tests: WEEKLY_DATA
        };
        aiScriptNode.textContent = JSON.stringify(fullPayload, null, 2);
    }
    
    // Set the weekly label
    const weekLabel = document.getElementById('week-label');
    if(weekLabel && typeof WEEKLY_DATA !== 'undefined') {
        weekLabel.textContent = `${WEEKLY_DATA.week_start} to ${WEEKLY_DATA.week_end}`;
    }

    initScorecard();
    renderGrids();
    initNav();
});

function initScorecard() {
    const retrospective = PREDICTIONS.filter(p => p.status === 'confirmed').length;
    const falsified = PREDICTIONS.filter(p => p.status === 'falsified').length;
    const advance   = PREDICTIONS.filter(p => p.status === 'pending').length;
    const weeklyCount = typeof WEEKLY_DATA !== 'undefined' ? WEEKLY_DATA.predictions.length : 0;
    
    const html = `
        <div class="score-hud"><span>${retrospective}</span> WINS</div>
        <div class="score-hud" style="color:var(--accent-blue);"><span>${weeklyCount}</span> LIVE TESTS</div>
        <div class="score-hud"><span>${advance}</span> PENDING</div>
        <div class="score-hud" style="color:var(--status-falsified)"><span>${falsified}</span> FALSIFIED</div>
    `;
    
    document.getElementById('scorecard').innerHTML = html;
}

function createCardHTML(p, isWeekly = false) {
    let resultLine = '';
    if (p.status !== 'pending') {
        resultLine = `
        <div style="margin-top:1rem; padding-top:1rem; border-top:1px dashed var(--border);">
            <div class="data-col">
                <span class="data-label" style="color:var(--status-${p.status})">RESULT:</span>
                <span class="data-val">${p.result_value !== null ? p.result_value : ''} (${p.result_date ? p.result_date.split('T')[0] : ''})</span>
            </div>
        </div>`;
    }

    const testDateDisplay = isWeekly ? 'Live This Week' : (p.test_date ? p.test_date.split('T')[0] : 'Ongoing');

    return `
    <div class="pred-card">
        <div class="card-header">
            <span class="id-badge">${p.id}</span>
            <span class="status-badge ${p.status}">${p.status}</span>
        </div>
        <h3 class="card-title">${p.title}</h3>
        <p class="card-desc">${p.description}</p>
        
        <div class="data-grid">
            <div class="data-col">
                <span class="data-label">TARGET</span>
                <span class="data-val" style="color:var(--accent-gold); font-size:1rem;">${testDateDisplay}</span>
            </div>
            <div class="data-col">
                <span class="data-label">PREDICTION</span>
                <span class="data-val">${p.prediction.value !== null ? p.prediction.value : ''} <span style="font-size:0.8rem">${p.prediction.unit || ''}</span></span>
            </div>
        </div>
        
        ${resultLine}
        
        <div class="card-actions">
            <div class="mech-text"><strong>Mechanism:</strong> ${p.mechanism}</div>
            <div class="mech-text" style="margin-bottom:0.75rem;"><strong>Source:</strong> ${p.data_source || 'INTERMAGNET'}</div>
            
            ${isWeekly ? `<a href="#" class="verify-btn" onclick="alert('Verification protocol will connect to: ${p.data_source}\\n\\nWaiting for Claude API implementation to pull live data.'); return false;">VERIFY LIVE DATA</a>` : ''}
            
            <div class="hash-foot">SHA256: ${p.sha256}</div>
        </div>
    </div>
    `;
}

function renderGrids() {
    const confirmedGrid = document.getElementById('confirmed-grid');
    const pendingGrid = document.getElementById('pending-grid');
    const weeklyGrid = document.getElementById('weekly-grid');

    // 1. Render the Long-Term arrays
    let confHTML = '', pendingHTML = '';
    PREDICTIONS.forEach(p => {
        const card = createCardHTML(p, false);
        if (p.status === 'confirmed') confHTML += card;
        if (p.status === 'pending') pendingHTML += card;
    });

    if (confirmedGrid) confirmedGrid.innerHTML = confHTML;
    if (pendingGrid) pendingGrid.innerHTML = pendingHTML;

    // 2. Render the new Weekly active tests
    let weekHTML = '';
    if (typeof WEEKLY_DATA !== 'undefined' && WEEKLY_DATA.predictions) {
        WEEKLY_DATA.predictions.forEach(p => {
            weekHTML += createCardHTML(p, true);
        });
    }
    
    if (weeklyGrid) weeklyGrid.innerHTML = weekHTML || '<p>No weekly data loaded.</p>';
}

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
}
