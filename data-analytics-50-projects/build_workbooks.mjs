// Runtime: @oai/artifact-tool in the Codex primary Node environment.
// Copy this builder to a temporary directory with a node_modules symlink to
// CODEX_PRIMARY_RUNTIME_NODE_MODULES, then run with collection root and case ID.
import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.argv[2];
const id=Number(process.argv[3]);
const p=JSON.parse(await fs.readFile(path.join(root,'excel_inputs.json'),'utf8')).find(p=>p.id===id);
const wb=Workbook.create();
const dash=wb.worksheets.add('Analysis');
const raw=wb.worksheets.add('Inputs');
const notes=wb.worksheets.add('Read Me');
const count=p.rows.length+1;
raw.getRange(`A1:D${count}`).values=[['Dimension','Sales','Profit','Quantity'],...p.rows];
raw.getRange('A1:D1').format={fill:'#142C49',font:{bold:true,color:'#FFFFFF'}};
raw.getRange(`A1:A${count}`).format.columnWidth=27;
raw.getRange(`B1:D${count}`).format.columnWidth=18;
raw.getRange(`B2:C${count}`).setNumberFormat('#,##0.00;[Red](#,##0.00)');
raw.getRange(`D2:D${count}`).setNumberFormat('#,##0');
raw.freezePanes.freezeRows(1);
raw.tables.add(`A1:D${count}`,true,'SourceRows');
dash.showGridLines=false; notes.showGridLines=false;
dash.getRange('A1:M3').merge();dash.getRange('A1').values=[[p.title]];
dash.getRange('A1:M3').format={fill:'#142C49',font:{bold:true,color:'#FFFFFF',size:20},rowHeight:23};
dash.getRange('A4:M4').merge();dash.getRange('A4').values=[['SUPERSTORE | '+p.dimension+' | 9,994 source lines | Md Adib Azam']];
dash.getRange('A5:M5').merge();dash.getRange('A5').values=[['Sales is used as supplied; margin = total profit / total sales. Monetary units follow the source.']];
dash.getRange('A4:M5').format={font:{color:'#52647A',size:10},rowHeight:22};
dash.getRange('A7:D7').values=[['Total sales','Total profit','Total units','Overall margin']];
dash.getRange('A8:D8').formulas=[[`=SUM('Inputs'!B2:B${count})`,`=SUM('Inputs'!C2:C${count})`,`=SUM('Inputs'!D2:D${count})`,'=IFERROR(B8/A8,0)']];
dash.getRange('A7:D8').format={fill:'#E8F4F3',font:{bold:true,color:'#075E63'},rowHeight:28};
dash.getRange('A8:B8').setNumberFormat('#,##0.00');dash.getRange('C8').setNumberFormat('#,##0');dash.getRange('D8').setNumberFormat('0.0%');
dash.getRange('A11:E11').values=[['Group','Sales','Profit','Quantity','Margin']];
dash.getRange('A11:E11').format={fill:'#087E8B',font:{bold:true,color:'#FFFFFF'},rowHeight:25};
for(let i=0;i<p.summary.length;i++){
  const r=12+i;
  dash.getRange(`A${r}`).values=[[p.summary[i][0]]];
  dash.getRange(`B${r}:E${r}`).formulas=[[
   `=SUMIF('Inputs'!$A$2:$A$${count},A${r},'Inputs'!$B$2:$B$${count})`,
   `=SUMIF('Inputs'!$A$2:$A$${count},A${r},'Inputs'!$C$2:$C$${count})`,
   `=SUMIF('Inputs'!$A$2:$A$${count},A${r},'Inputs'!$D$2:$D$${count})`,
   `=IFERROR(C${r}/B${r},0)`]];
}
const end=11+p.summary.length;
dash.getRange(`B12:C${end}`).setNumberFormat('#,##0.00;[Red](#,##0.00)');
dash.getRange(`D12:D${end}`).setNumberFormat('#,##0');dash.getRange(`E12:E${end}`).setNumberFormat('0.0%');
dash.getRange(`C12:C${end}`).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE8E6',font:{color:'#AE2721'}}});
dash.getRange('A1:A65').format.columnWidth=27;dash.getRange('B1:C65').format.columnWidth=20;
dash.getRange('D1:E65').format.columnWidth=17;dash.getRange('F1:M65').format.columnWidth=10;
dash.getRange(`A12:E${end}`).format.rowHeight=23;
const chart=dash.charts.add(p.dimension.startsWith('order_')?'line':'bar',{title:'Sales by '+p.dimension.replaceAll('_',' '),hasLegend:false});
const series=chart.series.add('Sales');series.categoryFormula=`'Analysis'!$A$12:$A$${end}`;series.formula=`'Analysis'!$B$12:$B$${end}`;series.fill='#087E8B';
if(['state','sub_category'].includes(p.dimension)){
 dash.getRange('G34:H34').values=[['Top 10 groups by sales','Sales']];
 for(let k=0;k<10;k++){
  const r=35+k;
  dash.getRange(`H${r}`).formulas=[[`=LARGE(B12:B${end},${k+1})`]];
  dash.getRange(`G${r}`).formulas=[[`=INDEX(A12:A${end},MATCH(H${r},B12:B${end},0))`]];
 }
 series.categoryFormula="'Analysis'!$G$35:$G$44";series.formula="'Analysis'!$H$35:$H$44";
}
chart.title=(['state','sub_category'].includes(p.dimension)?'Top 10: ':'')+'Sales by '+p.dimension.replaceAll('_',' ');
chart.hasLegend=false;
chart.setPosition('G11','N29');chart.yAxis={numberFormatCode:'#,##0',min:0};
chart.xAxis={axisType:'textAxis',tickLabelInterval:p.dimension==='order_month'?6:1};
chart.titleTextStyle.fontSize=12;
notes.getRange('A1:F2').merge();notes.getRange('A1').values=[['SOURCE, METHOD & REFRESH']];
notes.getRange('A1:F2').format={fill:'#142C49',font:{bold:true,color:'#FFFFFF'},rowHeight:25};
const lines=[
 'Source: Sample - Superstore (1)(2).csv; original bytes and SHA-256 are in the project repository.',
 'Inputs contains all 9,994 source lines projected to this case’s grouping field, Sales, Profit and Quantity.',
 'No discount is applied again. Order line counts are not described as order counts.',
 'Input numbers are editable. Summary values and native chart series are driven by formulas.',
 'For new rows or new groups, extend formula ranges and group labels, or rerun the builder.',
 'Group labels are a source snapshot. This workbook uses SUMIF, not a native PivotTable.',
 'No assumption of INR or currency conversion. Money follows source monetary units.',
 'Profit may be negative. Red cells indicate losses, not missing values.',
 'Reconcile totals: Sales 2,297,200.8603; Profit 286,397.0217; Quantity 37,873.',
 'See README.md and METRIC_DEFINITIONS.md for limitations and the reproducible Python/SQL reference.'
];
for(let i=0;i<lines.length;i++){notes.getRange(`A${i+4}:F${i+4}`).merge();notes.getRange(`A${i+4}`).values=[[lines[i]]];}
notes.getRange('A1:F15').format.columnWidth=19;notes.getRange('A4:F13').format={wrapText:true,rowHeight:40,font:{size:11,color:'#233B53'}};
const check=await wb.inspect({kind:'table',range:'Analysis!A7:E15',include:'values,formulas',tableMaxRows:9,tableMaxCols:5,maxChars:1500});
console.log(check.ndjson);
const values=dash.getRange(`B12:E${end}`).values;
for(let i=0;i<values.length;i++)for(let j=0;j<4;j++)if(Math.abs(Number(values[i][j])-p.summary[i][j+1])>1e-6)throw new Error(`Mismatch case ${id} row ${i} metric ${j}: ${values[i][j]} vs ${p.summary[i][j+1]}`);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A',options:{useRegex:true,maxResults:20},summary:'error scan'});
const out=path.join(root,p.folder);
await fs.mkdir(path.join(root,'outputs','superstore-qa'),{recursive:true});
for(const [sheetName,range] of [['Analysis','A1:N30'],['Inputs','A1:D10'],['Read Me','A1:F14']]){
 const blob=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,'outputs','superstore-qa',`${id}-${sheetName.replaceAll(' ','_')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(out,'analysis.xlsx'));
await fs.writeFile(path.join(out,'workbook_checks.json'),JSON.stringify({id,formula_results_match_sql:true,groups:p.summary.length,input_rows:p.rows.length,inspect:check.ndjson,error_scan:errors.ndjson},null,2));
console.log('EXPORTED',id,p.title);
