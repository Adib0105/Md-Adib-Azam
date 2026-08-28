export const sample = {"capacity":100,"ticket_price":299,"registrations":[{"name":"Asha","tickets":2},{"name":"Kabir","tickets":1},{"name":"Riya","tickets":3}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const booked=sum(input.registrations.map(x=>x.tickets));return {booked,remaining:Math.max(input.capacity-booked,0),sold_out:booked>=input.capacity,revenue:booked*input.ticket_price,valid:booked<=input.capacity};
}
