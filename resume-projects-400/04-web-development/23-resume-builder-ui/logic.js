export const sample = {"resume":{"name":"Md Adib Azam","summary":"CST student and Python developer","skills":["Python","SQL","Excel"],"experience":[{"role":"Customer Support Executive","months":14}],"education":"Diploma in CST"}};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const r=input.resume,checks={name:!!r.name,summary:(r.summary||"").length>=30,skills:(r.skills||[]).length>=3,experience:(r.experience||[]).length>0,education:!!r.education};return {completeness_pct:pct(Object.values(checks).filter(Boolean).length,Object.keys(checks).length),checks,preview:{heading:r.name,skills:(r.skills||[]).join(", "),experience_count:(r.experience||[]).length}};
}
