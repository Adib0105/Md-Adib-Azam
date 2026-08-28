export const sample = {"amount":1000,"from":"INR","to":"USD","rates":{"INR":1,"USD":0.012,"EUR":0.0105}};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  if(!(input.from in input.rates)||!(input.to in input.rates))throw new Error("missing rate");const inBase=input.amount/input.rates[input.from],converted=inBase*input.rates[input.to];return {amount:input.amount,from:input.from,to:input.to,converted:round(converted),rate_source:"user supplied"};
}
