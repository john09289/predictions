// DOME COSMOLOGY - VANILLA JS FRONTEND

document.addEventListener('DOMContentLoaded', async () => {
    // Inject master data into the hidden LD+JSON script tag for AI scrapers 
    const aiScriptNode = document.getElementById('dome-predictions-data');
    if (aiScriptNode) {
        const fullPayload = {
            metadata: { version: "V49.2", updated: new Date().toISOString() },
            master_predictions: typeof PREDICTIONS !== 'undefined' ? PREDICTIONS : [],
            weekly_active_tests: typeof WEEKLY_DATA !== 'undefined' ? WEEKLY_DATA : {}
        };
        aiScriptNode.textContent = JSON.stringify(fullPayload, null, 2);
    }
    
    // Set the weekly label
    const weekLabel = document.getElementById('week-label');
    if(weekLabel && typeof WEEKLY_DATA !== 'undefined') {
        weekLabel.textContent = `${WEEKLY_DATA.week_start} to ${WEEKLY_DATA.week_end}`;
    }

    try {
        const resArgs = await fetch('api/current/results.json');
        if (resArgs.ok) {
            window.RAW_RESULTS = await resArgs.json();
        } else {
            console.warn("Could not load api/current/results.json, falling back to empty.");
            window.RAW_RESULTS = [];
        }
    } catch (e) {
        console.error("Fetch failed", e);
        window.RAW_RESULTS = [];
    }

    // Attempt to compute the scored results manually
    window.SCORED_RESULTS = [];
    const allPreds = (typeof PREDICTIONS !== 'undefined' ? PREDICTIONS : []).concat(
        typeof WEEKLY_DATA !== 'undefined' ? WEEKLY_DATA.predictions || [] : []
    );
    const predMap = {};
    allPreds.forEach(p => predMap[p.id] = p);

    window.RAW_RESULTS.forEach(r => {
        let p = predMap[r.id];
        let sr = null;
        if (p && typeof scoreResult === 'function') {
            sr = scoreResult(p, r.observed);
        }
        
        let vr = sr ? sr.verdict.toLowerCase() : r.auto_verdict;
        // Merge them
        window.SCORED_RESULTS.push({
            ...r,
            auto_verdict: vr || r.auto_verdict,
            computed_score: sr
        });
    });

    initScorecard(window.SCORED_RESULTS);
    renderGrids(window.SCORED_RESULTS);
    initNav();
});

function computeScorecard(results) {
  return {
    wins: results.filter(r => {
      const v = (r.auto_verdict || "").toLowerCase();
      return ['confirmed', 'confirmed_marginal', 'confirmed_strong', 'overshoot_investigate'].includes(v);
    }).length,
      
    below_threshold: results.filter(r => 
      (r.auto_verdict || "").toLowerCase() === 'below_detection_threshold'
      ).length,
      
    investigating: results.filter(r =>
      (r.auto_verdict || "").toLowerCase() === 'overshoot_investigate'
      ).length,
      
    falsified: results.filter(r =>
      ((r.auto_verdict || "").toLowerCase() === 'falsified' && r.counts_against_model === true)
      ).length,
      
    pending: results.filter(r =>
      (r.auto_verdict || "").toLowerCase() === 'pending'
      ).length
  }
}

function initScorecard(results) {
    if (!results || results.length === 0) {
        document.getElementById('scorecard').innerHTML = '<div class="score-hud">Loading...</div>';
        return;
    }

    const scores = computeScorecard(results);
    const pendingTotal = typeof PREDICTIONS !== 'undefined' ? PREDICTIONS.filter(p => !p.scoring_matrix || p.status === 'pending').length : 0;
    const activeTestCount = typeof WEEKLY_DATA !== 'undefined' && WEEKLY_DATA.predictions ? WEEKLY_DATA.predictions.length : 0;
    
    // The user rules strictly states the wins, investigating, falsified must come exactly from the results array computations.
    const html = `
        <div class="score-hud"><span>${scores.wins}</span> WINS</div>
        <div class="score-hud" style="color:var(--accent-blue);"><span>${activeTestCount}</span> LIVE TESTS</div>
        <div class="score-hud"><span>${pendingTotal}</span> PENDING</div>
        <div class="score-hud" style="color:var(--status-falsified)"><span>${scores.falsified}</span> FALSIFIED</div>
    `;
    
    document.getElementById('scorecard').innerHTML = html;
}

function buildClaimsTable(computed_score) {
    if (!computed_score || !computed_score.claim_breakdown || computed_score.claim_breakdown.length === 0) return '';
    let rows = computed_score.claim_breakdown.map(c => `
      <div style="display:flex; justify-content:space-between; padding:0.25rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
        <span style="font-size:0.85rem; color:var(--text-secondary);">${c.claim}</span>
        <span style="font-size:0.85rem; font-weight:bold; ${c.result === 'CORRECT' ? 'color:#34d399;' : 'color:#ef4444;'}">
          ${c.result === 'CORRECT' ? '✓' : '✗'} [${c.result === 'CORRECT' ? '+'+c.points : c.points}]
        </span>
      </div>
    `).join('');
    
    return `
      <div class="glass-card" style="background: rgba(0,0,0,0.3); padding: 1rem; border: 1px dashed var(--border-subtle); margin-bottom: 1rem;">
          <div style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.5rem; text-transform: uppercase; display:flex; justify-content:space-between;">
             <span>MECHANISM CONFIRMATION MATRIX</span>
             <span style="color:var(--text-primary)">Score: ${computed_score.total_score}/${computed_score.max_score} (${Math.round(computed_score.percentage*100)}%)</span>
          </div>
          ${rows}
          <div style="margin-top:0.75rem; font-size:0.85rem; color:var(--accent-sky);">
             <strong>Model-Distinguishing Claims:</strong> ${computed_score.model_distinguishing_passed} / ${computed_score.model_distinguishing_total} Passed
          </div>
      </div>
    `;
}

function createCardHTML(p, resultMap, isWeekly = false) {
    let resultLine = '';
    let claimsHTML = '';
    const resNode = resultMap[p.id];
    
    let displayLabel = "PENDING";
    let statusClass = "pending";
    let colorStyle = "color:var(--text-muted);";
    
    if (resNode && resNode.auto_verdict) {
        displayLabel = resNode.display_label || resNode.auto_verdict.replace(/_/g, ' ').toUpperCase();
        statusClass = resNode.auto_verdict.replace(/_/g, '-');
        
        const vd = resNode.auto_verdict.toLowerCase();
        if(['confirmed', 'confirmed_marginal', 'confirmed_strong'].includes(vd)) {
            colorStyle = 'color:#34d399;';
        } else if (vd === 'below_detection_threshold') {
            colorStyle = 'color:#eab308;';
        } else if (vd === 'falsified') {
            colorStyle = 'color:#ef4444;';
        } else if (vd === 'overshoot_investigate') {
            colorStyle = 'color:#0ea5e9;';
        } else if (vd === 'inconclusive') {
            colorStyle = 'color:#9ca3af;';
        }

        const missingNote = vd === 'below_detection_threshold' ? 
            `<div style="font-size:0.85rem; color:#eab308; margin-top:0.25rem;">Signal below detection limit - prediction untestable at this sensitivity. Not a model failure.</div>` : '';
            
        const overshootNote = (resNode.overshoot_ratio && resNode.overshoot_ratio > 1.0 && (resNode.direction_correct || resNode.computed_score)) ?
            `<div style="font-size:0.85rem; color:#34d399; margin-top:0.25rem;">Signal ${resNode.overshoot_ratio}x stronger than predicted - mechanism confirmed, magnitude being refined.</div>` : '';
            
        const sigmaText = resNode.sigma_distance !== undefined && resNode.sigma_distance > 0 ? 
            `<span style="margin-right: 0.75rem;">${resNode.sigma_distance}σ from prediction</span>` : '';
            
        const snrVal = (resNode.observed && resNode.observed.snr) ? resNode.observed.snr : null;
        const snrSuff = (snrVal >= 2.0) || resNode.snr_sufficient;
        const snrText = snrVal ? 
            `<span style="margin-right: 0.75rem;">SNR: ${snrVal} (${snrSuff ? 'detectable' : 'sub-threshold'})</span>` : '';
            
        const dirCorrect = resNode.direction_correct;
        const dirText = dirCorrect !== undefined ? 
            `<span>Direction: ${dirCorrect ? '✓ Correct' : '✗ Wrong'}</span>` : '';

        const obsVal = resNode.observed && resNode.observed.value !== undefined ? resNode.observed.value : (p.result_value || resNode.observed?.peak_nT || '');

        resultLine = `
        <div class="data-matrix" style="border-top:none; padding-top:0; margin-top:-0.5rem;">
            <div class="data-row">
                <span class="data-label" style="${colorStyle}">OBSERVED RESULT</span>
                <span class="data-value" style="${colorStyle}">${obsVal}</span>
            </div>
            ${(sigmaText || snrText || dirText) ? `<div style="font-size: 0.8rem; color: var(--text-secondary); margin-top:0.25rem;">${sigmaText}${snrText}${dirText}</div>` : ''}
            ${missingNote}
            ${overshootNote}
        </div>`;
        
        claimsHTML = buildClaimsTable(resNode.computed_score);

    } else if (p.status !== 'pending' && p.result_value) {
        // Fallback for missing JSON results
        const isSuccessful = p.status === 'confirmed';
        colorStyle = isSuccessful ? 'color:#34d399;' : 'color:#ef4444;';
        displayLabel = p.status.toUpperCase();
        statusClass = p.status;
        resultLine = `
        <div class="data-matrix" style="border-top:none; padding-top:0; margin-top:-0.5rem;">
            <div class="data-row">
                <span class="data-label" style="${colorStyle}">OBSERVED RESULT</span>
                <span class="data-value" style="${colorStyle}">${p.result_value !== null ? p.result_value : ''}</span>
            </div>
        </div>`;
    }

    const testDateDisplay = isWeekly ? 'Live This Week' : (p.test_date ? p.test_date.split('T')[0] : 'Ongoing');
    const predVal = p.point_prediction ? p.point_prediction.value : (p.prediction ? p.prediction.value : (p.prediction_nT || ''));
    const unitVal = p.prediction ? (p.prediction.unit || '') : '';

    return `
    <div class="glass-card">
        <div class="card-topbar">
            <span class="id-tag">${p.id}</span>
            <div class="status-indicator status-${statusClass}" style="${colorStyle}">
                <div class="status-dot" style="background:${colorStyle.split(':')[1].replace(';','')}"></div>
                ${displayLabel}
            </div>
        </div>
        <h3 class="card-title">${p.title || p.station}</h3>
        <p class="card-desc">${p.description || (p.mechanism ? p.mechanism.description : '')}</p>
        
        <div class="data-matrix">
            <div class="data-row">
                <span class="data-label">TARGET WINDOW</span>
                <span class="data-value accent">${testDateDisplay}</span>
            </div>
            <div class="data-row">
                <span class="data-label">MODEL PREDICTION</span>
                <span class="data-value">${predVal !== null && predVal !== undefined ? predVal : ''} <span style="font-size:0.8rem; color:var(--text-muted)">${unitVal}</span></span>
            </div>
        </div>
        
        ${resultLine}
        ${claimsHTML}
        
        <div class="card-mechanism" style="margin-bottom: 0.5rem;">
            <div style="margin-bottom:0.25rem;"><strong style="color:var(--text-primary)">Mechanism:</strong> ${p.mechanism && p.mechanism.description ? p.mechanism.description : 'Empirical Validation'}</div>
            <div><strong style="color:var(--text-primary)">Verification Anchor:</strong> ${p.data_source || 'INTERMAGNET'}</div>
        </div>

        ${p.derivation ? `
        <div class="glass-card" style="background: rgba(0,0,0,0.1); padding: 1rem; border: 1px dashed var(--border-subtle); margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.5rem; text-transform: uppercase;">DERIVATION MECHANISM</div>
            <div style="font-size: 0.9rem; margin-bottom: 0.25rem; font-family:monospace; color:var(--accent-purple)"><strong style="color:var(--text-primary)">Formula:</strong> ${p.derivation.formula}</div>
        </div>
        ` : ''}
            
        ${isWeekly ? `<a href="proofs/weekly_predictions_${typeof WEEKLY_DATA !== 'undefined' ? WEEKLY_DATA.week_start : ''}.json.ots" download class="btn-verify btn-primary" style="margin-top:auto;" data-proof-type="opentimestamps" data-sha256="${p.sha256}" title="Download Bitcoin blockchain anchor proof">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            GET CRYPTOGRAPHIC PROOF (.OTS)
        </a>` : ''}
            
        <div class="sha-fingerprint">SHA-256: ${p.sha256 || p.manifest_sha256}</div>
    </div>
    `;
}

function renderGrids(results) {
    const confirmedGrid = document.getElementById('confirmed-grid');
    const pendingGrid = document.getElementById('pending-grid');
    const weeklyGrid = document.getElementById('weekly-grid');

    const resultMap = {};
    if(results) {
        results.forEach(r => resultMap[r.id] = r);
    }

    // 1. Render the Long-Term arrays
    let confHTML = '', pendingHTML = '';
    if (typeof PREDICTIONS !== 'undefined') {
        PREDICTIONS.forEach(p => {
            const resNode = resultMap[p.id];
            const isConfirmed = resNode ? ['confirmed', 'confirmed_marginal', 'confirmed_strong', 'overshoot_investigate'].includes(resNode.auto_verdict || '') : p.status === 'confirmed';
            const isFalsified = resNode ? (resNode.auto_verdict === 'falsified') : p.status === 'falsified';
            
            const card = createCardHTML(p, resultMap, false);
            if (isConfirmed || isFalsified || (resNode && resNode.auto_verdict && resNode.auto_verdict !== 'pending')) {
                confHTML += card;
            } else {
                pendingHTML += card;
            }
        });
    }

    if (confirmedGrid) confirmedGrid.innerHTML = confHTML;
    if (pendingGrid) pendingGrid.innerHTML = pendingHTML;

    // 2. Render the new Weekly active tests
    let weekHTML = '';
    if (typeof WEEKLY_DATA !== 'undefined' && WEEKLY_DATA.predictions) {
        WEEKLY_DATA.predictions.forEach(p => {
            weekHTML += createCardHTML(p, resultMap, true);
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
            if (document.getElementById(target)) {
                document.getElementById(target).classList.add('active');
            }
        });
    });
}
