const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));
console.log("Total in allSwitches:", allSwitches.length);

// Verify key fixes
const checks = ['S7706', 'S7712', 'S8700', 'CE9865', 'S6520X-54QC-HI', 'CE9865-8', 'S6520X-54XG-EI', 'CE6881-48S6CQ-H'];
for (const c of checks) {
    const matches = allSwitches.filter(sw => sw.model.toLowerCase().includes(c.toLowerCase()));
    for (const sw of matches) {
        console.log(`${sw.model}: cap=${sw.switching_capacity}, fwd=${sw.forwarding_rate}`);
    }
}
