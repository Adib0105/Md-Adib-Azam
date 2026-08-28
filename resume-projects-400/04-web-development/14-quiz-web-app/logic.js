export const sample = {"questions":[{"id":"q1","answer":"B","explanation":"Use semantic HTML."},{"id":"q2","answer":"A","explanation":"Labels identify inputs."}],"answers":{"q1":"B","q2":"C"}};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const review=input.questions.map(q=>({id:q.id,correct:input.answers[q.id]===q.answer,answer:q.answer,explanation:q.explanation}));return {score:review.filter(x=>x.correct).length,out_of:review.length,percentage:pct(review.filter(x=>x.correct).length,review.length),missed:review.filter(x=>!x.correct)};
}
