const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

// Check problematic switches
const targets = ['S7706', 'S7712', 'S8700', 'CE9865', 'CE6881', 'S6520X', 'S6850', 'S6730-S48X6Q', 'S5731', 'S5590', 'S5135S', 'S5310-24GT4XS-P', 'S2910', 'S6526XE'];

for (const target of targets) {
    const matches = allSwitches.filter(sw => sw.model.toLowerCase().includes(target.toLowerCase()));
    console.log(`\n=== ${target} (${matches.length}款) ===`);
    for (const sw of matches) {
        console.log(`  ${sw.model} (${sw.vendor}/${sw.tier})`);
        console.log(`    cap=${sw.switching_capacity}, fwd=${sw.forwarding_rate}`);
        console.log(`    ports=${sw.ports}`);
        console.log(`    exp=${sw.expansion_slots}, poe=${sw.poe_support}`);
    }
}
