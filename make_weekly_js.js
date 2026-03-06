const fs = require('fs');
const json = fs.readFileSync('proofs/weekly_predictions_2026-03-06.json', 'utf8');
fs.writeFileSync('weekly.js', `const WEEKLY_DATA = ${json};`);
console.log('weekly.js generated.');
