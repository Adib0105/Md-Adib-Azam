export const sample = {"product":"Wireless Headset","unit_price":2499,"quantity":3,"tax_rate":0.18,"discount_threshold":5000,"discount_rate":0.1};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const subtotal=input.unit_price*input.quantity,discount=subtotal>=input.discount_threshold?subtotal*input.discount_rate:0,tax=(subtotal-discount)*input.tax_rate;return {product:input.product,subtotal,money_discount:round(discount),tax:round(tax),total:round(subtotal-discount+tax)};
}
