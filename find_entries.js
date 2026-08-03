const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));
console.log("Total switches in allSwitches:", allSwitches.length);

// Find specific models
const targets = ['S7706', 'S7712', 'S8700', 'CE9865', 'CE6881', 'S6520X-54QC-HI', 'S6520X-54HF-EI', 'S6850', 'S5735-L48T4XE', 'S6730-S48X6Q'];
for (const t of targets) {
    const matches = allSwitches.filter(sw => sw.model.toLowerCase().includes(t.toLowerCase()));
    for (const sw of matches) {
        console.log(`\n${sw.model} (${sw.vendor}/${sw.tier}):`);
        console.log(`  cap=${sw.switching_capacity}`);
        console.log(`  fwd=${sw.forwarding_rate}`);
        console.log(`  ports=${sw.ports}`);
        console.log(`  exp=${sw.expansion_slots}`);
    }
}
