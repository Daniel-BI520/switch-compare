const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Find the allSwitches array boundaries
const swStart = html.indexOf('const allSwitches = [');
const swEnd = html.indexOf('];', swStart) + 2;
const allSwitchesStr = html.substring(swStart, swEnd);

// Parse it
const allSwitchesCode = 'var allSwitches = ' + allSwitchesStr.replace('const allSwitches = ', '');
eval(allSwitchesCode);
console.log("Before fix:", allSwitches.length, "switches");

// Fix data
function fixSwitch(modelSearch, updates) {
    let found = 0;
    for (const sw of allSwitches) {
        if (sw.model.toLowerCase().includes(modelSearch.toLowerCase())) {
            for (const [key, val] of Object.entries(updates)) {
                sw[key] = val;
            }
            found++;
            console.log(`  ✅ Fixed: ${sw.model} → ${JSON.stringify(updates)}`);
        }
    }
    if (!found) console.log(`  ⚠️ Not found: ${modelSearch}`);
    return found;
}

// 1. S7706 forwarding rate
fixSwitch('S7706', { forwarding_rate: '57600Mpps/115200Mpps' });

// 2. S7712 forwarding rate
fixSwitch('S7712', { forwarding_rate: '115200Mpps/230400Mpps' });

// 3. S8700-6 capacity and forwarding rate
fixSwitch('S8700-6', { 
    switching_capacity: '336Tbps/1344Tbps',
    forwarding_rate: '230400Mpps'
});

// 4. CE9865-4C capacity
fixSwitch('CE9865-4C', {
    switching_capacity: '576Tbps/2304Tbps',
    forwarding_rate: '288000Mpps'
});

// 5-7. S6520X HI variants forwarding rate
fixSwitch('S6520X-54QC-HI', { forwarding_rate: '2520Mpps/3240Mpps' });
fixSwitch('S6520X-54HC-HI', { forwarding_rate: '2520Mpps/3240Mpps' });
fixSwitch('S6520X-54HF-HI', { forwarding_rate: '2520Mpps/3240Mpps' });

// 8-9. S6520X EI variants
fixSwitch('S6520X-54QC-EI', { forwarding_rate: '2160Mpps/2520Mpps' });
fixSwitch('S6520X-54HF-EI', { forwarding_rate: '2160Mpps' });
fixSwitch('S6520X-54HC-EI', { forwarding_rate: '2160Mpps' });

// Add new switches
const newSwitches = [
    {
        vendor: "华为", series: "CloudEngine 9800 系列", model: "CE9865-8", tier: "核心",
        switching_capacity: "576Tbps/2304Tbps", forwarding_rate: "288000Mpps",
        ports: "8个业务槽位，支持256x100GE或64x400GE", poe_support: "否",
        expansion_slots: "8个业务槽", power_redundancy: "2+2冗余", fan_redundancy: "冗余",
        url: "https://e.huawei.com/cn/products/switches/data-center-switches/ce9800",
        features: "CLOS交换、RoCE V1/V2、BGP-EVPN、PFC/AI ECN、Telemetry、MACsec",
        is_hot: true, is_new: true
    },
    {
        vendor: "H3C", series: "S6520X EI 系列", model: "S6520X-54XG-EI", tier: "汇聚",
        switching_capacity: "2.56Tbps/25.6Tbps", forwarding_rate: "2160Mpps",
        ports: "48个1/10GE SFP+端口，6个40/100GE QSFP28端口", poe_support: "否",
        expansion_slots: "2个扩展槽", power_redundancy: "1+1冗余", fan_redundancy: "冗余",
        url: "https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X/",
        features: "万兆汇聚、IRF2堆叠、VXLAN、M-LAG、BGP EVPN、SDN",
        is_hot: false, is_new: true
    },
    {
        vendor: "华为", series: "CloudEngine 6881 系列", model: "CE6881-48S6CQ-H", tier: "接入",
        switching_capacity: "6.75Tbps/96Tbps", forwarding_rate: "4800Mpps",
        ports: "48个10GE SFP+ + 6个100GE QSFP28", poe_support: "否",
        expansion_slots: "0", power_redundancy: "1+1冗余", fan_redundancy: "冗余",
        url: "https://e.huawei.com/cn/products/switches/data-center-switches/ce6800",
        features: "VXLAN、BGP-EVPN、M-LAG、Telemetry、DCBX/PFC/ETS、高配版",
        is_hot: false, is_new: true
    }
];

for (const ns of newSwitches) {
    if (!allSwitches.find(sw => sw.model === ns.model)) {
        allSwitches.push(ns);
        console.log(`  ✅ Added: ${ns.model}`);
    } else {
        console.log(`  ⚠️ Already exists: ${ns.model}`);
    }
}

console.log("After fix:", allSwitches.length, "switches");

// Rebuild the allSwitches section
const newAllSwitchesStr = 'const allSwitches = ' + JSON.stringify(allSwitches, null, 2) + '];';
html = html.substring(0, swStart) + newAllSwitchesStr + html.substring(swEnd);

fs.writeFileSync('index.html', html, 'utf8');
console.log("\n✅ index.html updated with allSwitches fixes");
