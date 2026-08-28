export const sample = {"today":"2026-08-28","lessons":[{"title":"HTML","complete":true,"due":"2026-08-20"},{"title":"CSS","complete":true,"due":"2026-08-24"},{"title":"JavaScript","complete":false,"due":"2026-08-27"},{"title":"Accessibility","complete":false,"due":"2026-09-01"}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const complete=input.lessons.filter(x=>x.complete).length;return {completion_pct:pct(complete,input.lessons.length),overdue:input.lessons.filter(x=>!x.complete&&x.due<input.today).map(x=>x.title),next:input.lessons.find(x=>!x.complete)?.title||null};
}
