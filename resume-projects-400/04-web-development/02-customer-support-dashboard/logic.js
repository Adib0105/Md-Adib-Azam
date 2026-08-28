export const sample = {"tickets":[{"aht":320,"sla":true,"csat":5},{"aht":410,"sla":false,"csat":3},{"aht":280,"sla":true,"csat":4}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const n=input.tickets.length;return {tickets:n,sla_pct:pct(input.tickets.filter(x=>x.sla).length,n),avg_aht_seconds:avg(input.tickets.map(x=>x.aht)),csat:avg(input.tickets.map(x=>x.csat))};
}
