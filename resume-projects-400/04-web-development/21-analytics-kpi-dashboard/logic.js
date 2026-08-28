export const sample = {"sessions":[{"channel":"organic","sessions":1200,"conversions":72,"bounces":420},{"channel":"social","sessions":800,"conversions":24,"bounces":400},{"channel":"email","sessions":400,"conversions":48,"bounces":80}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const sessions=sum(input.sessions.map(x=>x.sessions)),conversions=sum(input.sessions.map(x=>x.conversions)),bounces=sum(input.sessions.map(x=>x.bounces));return {sessions,conversions,conversion_rate:pct(conversions,sessions),bounce_rate:pct(bounces,sessions),top_channel:[...input.sessions].sort((a,b)=>b.conversions/b.sessions-a.conversions/a.sessions)[0].channel};
}
