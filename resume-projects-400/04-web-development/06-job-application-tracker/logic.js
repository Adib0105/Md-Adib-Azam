export const sample = {"today":"2026-08-28","applications":[{"company":"Alpha","status":"Applied","follow_up":"2026-08-29"},{"company":"Beta","status":"Interview","follow_up":"2026-08-28"},{"company":"Gamma","status":"Rejected","follow_up":null}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const counts={};input.applications.forEach(x=>counts[x.status]=(counts[x.status]||0)+1);return {total:input.applications.length,status_counts:counts,follow_ups:input.applications.filter(x=>x.follow_up&&x.follow_up>=input.today&&x.status!=="Rejected").map(x=>x.company)};
}
