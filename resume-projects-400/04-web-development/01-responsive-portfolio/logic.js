export const sample = {"skill":"python","projects":[{"name":"Analytics","skills":["python","sql"]},{"name":"Landing Page","skills":["html","css"]},{"name":"Automation","skills":["python"]}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const visible=input.projects.filter(p=>input.skill==="all"||p.skills.includes(input.skill));return {filter:input.skill,count:visible.length,projects:visible.map(p=>p.name)};
}
