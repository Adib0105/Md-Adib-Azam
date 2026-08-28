export const sample = {"height_cm":175,"weight_kg":74};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const meters=input.height_cm/100,bmi=input.weight_kg/(meters*meters),category=bmi<18.5?"underweight":bmi<25?"healthy range":bmi<30?"overweight range":"high range";return {bmi:round(bmi),category,note:"Screening estimate only; not a diagnosis."};
}
