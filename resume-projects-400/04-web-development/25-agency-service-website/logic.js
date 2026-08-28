export const sample = {"services":[{"name":"Website","price":12000},{"name":"SEO Audit","price":3500},{"name":"Social Setup","price":2500}],"selected":["Website","SEO Audit"],"tax_rate":0.18};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const selected=input.services.filter(x=>input.selected.includes(x.name)),subtotal=sum(selected.map(x=>x.price)),tax=subtotal*input.tax_rate;return {line_items:selected,subtotal,tax:round(tax),grand_total:round(subtotal+tax),currency:"INR"};
}
