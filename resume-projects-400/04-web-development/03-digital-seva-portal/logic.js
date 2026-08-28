export const sample = {"services":[{"name":"Certificate","fee":120,"days":3},{"name":"Bill Payment","fee":20,"days":0},{"name":"Form Assistance","fee":80,"days":1}],"selected":["Certificate","Form Assistance"]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const rows=input.services.filter(x=>input.selected.includes(x.name));return {selected:rows.map(x=>x.name),total_fee:sum(rows.map(x=>x.fee)),maximum_turnaround_days:Math.max(0,...rows.map(x=>x.days))};
}
