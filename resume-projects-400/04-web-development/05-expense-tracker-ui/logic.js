export const sample = {"budget":10000,"expenses":[{"category":"food","amount":2200},{"category":"travel","amount":1300},{"category":"learning","amount":900},{"category":"food","amount":500}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const by_category={};input.expenses.forEach(x=>by_category[x.category]=(by_category[x.category]||0)+x.amount);const spent=sum(input.expenses.map(x=>x.amount));return {spent,remaining:input.budget-spent,by_category};
}
