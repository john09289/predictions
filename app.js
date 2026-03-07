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
    if (p.status !== 'pending' && p.verdict !== 'pending') {
        const isSuccessful = p.status === 'confirmed' || p.verdict === 'CONFIRMED' || p.verdict === 'CONFIRMED_MARGINAL';
        const colorClass = isSuccessful ? 'color:#34d399;' : (p.verdict === 'BELOW_DETECTION_THRESHOLD' ? 'color:#eab308;' : 'color:#ef4444;');
        resultLine = `
        <div class="data-matrix" style="border-top:none; padding-top:0; margin-top:-0.5rem;">
            <div class="data-row">
                <span class="data-label" style="${colorClass}">OBSERVED RESULT</span>
                <span class="data-value" style="${colorClass}">${p.result_value !== null ? p.result_value : ''} <span style="font-size:0.7rem; opacity:0.7">(${p.result_date ? p.result_date.split('T')[0] : ''})</span></span>
            </div>
        </div>`;
    }

    const testDateDisplay = isWeekly ? 'Live This Week' : (p.test_date ? p.test_date.split('T')[0] : 'Ongoing');

    const verdictVal = p.verdict || p.status || 'pending';
    const statusClass = verdictVal.toLowerCase().replace(/ /g, '_');
    const displayLabel = p.display_label || verdictVal.replace(/_/g, ' ');

    return `
    <div class="glass-card">
        <div class="card-topbar">
            <span class="id-tag">${p.id}</span>
            <div class="status-indicator status-${statusClass}">
                <div class="status-dot"></div>
                ${displayLabel}
            </div>
        </div>
        <h3 class="card-title">${p.title}</h3>
        <p class="card-desc">${p.description}</p>
        
        <div class="data-matrix">
            <div class="data-row">
                <span class="data-label">TARGET WINDOW</span>
                <span class="data-value accent">${testDateDisplay}</span>
            </div>
            <div class="data-row">
                <span class="data-label">MODEL PREDICTION</span>
                <span class="data-value">${p.prediction.value !== null ? p.prediction.value : ''} <span style="font-size:0.8rem; color:var(--text-muted)">${p.prediction.unit || ''}</span></span>
            </div>
        </div>
        
        ${resultLine}
        
        <div class="card-mechanism" style="margin-bottom: 0.5rem;">
            <div style="margin-bottom:0.25rem;"><strong style="color:var(--text-primary)">Mechanism:</strong> ${p.mechanism || 'Empirical Validation'}</div>
            <div><strong style="color:var(--text-primary)">Verification Anchor:</strong> ${p.data_source || 'INTERMAGNET'}</div>
        </div>

        ${p.mainstream_comparison ? `
        <div class="glass-card" style="background: rgba(0,0,0,0.3); padding: 1rem; border: 1px dashed var(--border-subtle); margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.5rem; text-transform: uppercase;">MAINSTREAM COMPARISON</div>
            <div style="font-size: 0.9rem; margin-bottom: 0.25rem;"><strong style="color:var(--text-primary)">Expected:</strong> ${p.mainstream_comparison.mainstream_expected}</div>
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong style="color:var(--text-primary)">Our Model:</strong> ${p.mainstream_comparison.our_prediction}</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; border-left: 2px solid var(--accent-sky); padding-left: 0.75rem;">${p.mainstream_comparison.context}</div>
        </div>
        ` : ''}
            
        ${isWeekly ? `<a href="proofs/weekly_predictions_${typeof WEEKLY_DATA !== 'undefined' ? WEEKLY_DATA.week_start : ''}.json.ots" download class="btn-verify btn-primary" style="margin-top:auto;" data-proof-type="opentimestamps" data-sha256="${p.sha256}" title="Download Bitcoin blockchain anchor proof">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            GET CRYPTOGRAPHIC PROOF (.OTS)
        </a>` : ''}
            
        <div class="sha-fingerprint">SHA-256: ${p.sha256}</div>
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
    const btns = document.querySelectorAll('.nav-pill');
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
