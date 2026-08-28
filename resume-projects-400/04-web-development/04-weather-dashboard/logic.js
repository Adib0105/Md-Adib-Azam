export const sample = {"city":"Howrah","readings":[{"temp":31,"rain_probability":80},{"temp":29,"rain_probability":60},{"temp":32,"rain_probability":20}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  return {city:input.city,average_temperature_c:avg(input.readings.map(x=>x.temp)),peak_rain_probability:Math.max(...input.readings.map(x=>x.rain_probability)),umbrella:input.readings.some(x=>x.rain_probability>=60)};
}
