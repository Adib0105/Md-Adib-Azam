export const sample = {"requested_minutes":30,"business_hours":{"start":540,"end":1020},"bookings":[{"start":600,"end":660},{"start":720,"end":750},{"start":900,"end":960}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const slots=[];for(let start=input.business_hours.start;start+input.requested_minutes<=input.business_hours.end;start+=input.requested_minutes){const end=start+input.requested_minutes;if(!input.bookings.some(b=>start<b.end&&b.start<end))slots.push({start,end});}return {duration_minutes:input.requested_minutes,available_slots:slots,count:slots.length};
}
