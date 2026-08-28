export const sample = {"leads":[{"name":"Alpha","fit":8,"engagement":7,"days_old":2},{"name":"Beta","fit":5,"engagement":3,"days_old":30},{"name":"Gamma","fit":9,"engagement":9,"days_old":1}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const leads=input.leads.map(x=>({...x,score:Math.max(0,round(x.fit*5+x.engagement*4-Math.min(x.days_old,30)))})).sort((a,b)=>b.score-a.score);return {leads,hot:leads.filter(x=>x.score>=70).map(x=>x.name),next_action:leads[0]?.name||null};
}
