export const sample = {"query":"password reset","faqs":[{"question":"How do I reset my password?","answer":"Use Forgot Password."},{"question":"How do I update email?","answer":"Open profile settings."},{"question":"Why is login blocked?","answer":"Contact support after repeated failures."}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const terms=input.query.toLowerCase().split(/\s+/);const ranked=input.faqs.map(x=>({...x,score:terms.filter(t=>(x.question+" "+x.answer).toLowerCase().includes(t)).length})).filter(x=>x.score).sort((a,b)=>b.score-a.score);return {query:input.query,count:ranked.length,results:ranked};
}
