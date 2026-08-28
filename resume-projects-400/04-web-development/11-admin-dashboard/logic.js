export const sample = {"metrics":[{"name":"Open Tickets","actual":18,"target":15,"lower_is_better":true},{"name":"CSAT","actual":4.5,"target":4.3,"lower_is_better":false},{"name":"On-Time Delivery","actual":92,"target":95,"lower_is_better":false}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const metrics=input.metrics.map(x=>({...x,met:x.lower_is_better?x.actual<=x.target:x.actual>=x.target,variance:round(x.actual-x.target)}));return {metrics,met_count:metrics.filter(x=>x.met).length,missed:metrics.filter(x=>!x.met).map(x=>x.name)};
}
