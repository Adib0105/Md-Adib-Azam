export const sample = {"questions":[{"topic":"phishing","correct":"B"},{"topic":"passwords","correct":"C"},{"topic":"updates","correct":"A"}],"answers":["B","A","A"]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const results=input.questions.map((q,i)=>({topic:q.topic,correct:q.correct===input.answers[i]}));return {score:results.filter(x=>x.correct).length,out_of:results.length,risk_level:results.filter(x=>x.correct).length===results.length?"low":"training recommended",review_topics:results.filter(x=>!x.correct).map(x=>x.topic)};
}
