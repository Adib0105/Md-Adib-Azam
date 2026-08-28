export const sample = {"wip_limit":2,"tasks":[{"title":"API","status":"Doing"},{"title":"Tests","status":"Doing"},{"title":"Docs","status":"Doing"},{"title":"Deploy","status":"Todo"},{"title":"Review","status":"Done"}]};
const round = value => Math.round((value + Number.EPSILON) * 100) / 100;
const sum = values => values.reduce((a,b)=>a+b,0);
const avg = values => values.length ? round(sum(values)/values.length) : 0;
const pct = (part,total) => total ? round(part/total*100) : 0;

export function calculate(input) {
  const board={Todo:[],Doing:[],Done:[]};input.tasks.forEach(x=>(board[x.status]??=[]).push(x.title));return {board,counts:Object.fromEntries(Object.entries(board).map(([k,v])=>[k,v.length])),wip_breach:board.Doing.length>input.wip_limit};
}
