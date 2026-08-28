export const sample = {"coupon":"SAVE10","valid_coupons":{"SAVE10":0.1},"free_shipping_at":2000,"shipping":99,"items":[{"name":"Mouse","qty":2,"price":699},{"name":"Keyboard","qty":1,"price":1299}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const subtotal=sum(input.items.map(x=>x.qty*x.price)),rate=input.valid_coupons[input.coupon]||0,discount=subtotal*rate,shipping=subtotal-discount>=input.free_shipping_at?0:input.shipping;return {subtotal,discount:round(discount),shipping,total:round(subtotal-discount+shipping),coupon_valid:rate>0};
}
