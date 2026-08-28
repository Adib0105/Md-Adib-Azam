export const sample = {"tag":"nature","images":[{"file":"rain.jpg","tags":["nature","weather"],"alt":"Rain falling on leaves"},{"file":"city.jpg","tags":["travel"],"alt":""},{"file":"river.jpg","tags":["nature"],"alt":"River at sunset"}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const visible=input.images.filter(x=>x.tags.includes(input.tag));return {tag:input.tag,visible,missing_alt:input.images.filter(x=>!x.alt.trim()).map(x=>x.file),accessible:input.images.every(x=>x.alt.trim())};
}
