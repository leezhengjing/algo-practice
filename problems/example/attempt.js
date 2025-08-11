const fs = require('fs');
const input = fs.readFileSync(0, 'utf8').trim();
const n = parseInt(input, 10);
console.log(n * n);