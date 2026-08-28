export const sample = {"items":[{"name":"Paneer Roll","veg":true,"qty":2,"price":140},{"name":"Chicken Biryani","veg":false,"qty":3,"price":240},{"name":"Cold Drink","veg":true,"qty":3,"price":40}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const subtotal=sum(input.items.map(x=>x.qty*x.price));return {lines:input.items.map(x=>({...x,line_total:x.qty*x.price})),vegetarian_options:input.items.filter(x=>x.veg).map(x=>x.name),subtotal,gst:round(subtotal*.05),total:round(subtotal*1.05)};
}
