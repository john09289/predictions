const fs = require('fs');
eval(fs.readFileSync('scoring.js', 'utf8'));

let prediction = {
    point_prediction: { value: null, uncertainty: null },
    scoring_matrix: [
        { claim: "Signal is correct polarity", weight: "HIGH", auto_check: "direction_correct", points_if_correct: 5, points_if_wrong: -5 },
        { claim: "Signal exceeds noise floor", weight: "HIGH", auto_check: "observed.snr >= 2.0", points_if_correct: 3, points_if_wrong: 0 },
        { claim: "Magnitude within 1-sigma", weight: "MEDIUM", auto_check: "sigma_distance <= 1.0", points_if_correct: 2, points_if_wrong: -1 }
    ]
};
let observed = { value: -17.6, snr: 4.0 };

console.log(scoreResult(prediction, observed));
