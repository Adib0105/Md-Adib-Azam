#!/usr/bin/env python3
from __future__ import annotations
import csv,json,math,sys
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean,stdev

def f(row,key):return float(row[key])
def round2(value):return round(float(value),2)
def pct(part,total):return round2(part/total*100) if total else 0
def group_sum(rows,key,value):
 out={}
 for row in rows:out[row[key]]=out.get(row[key],0)+f(row,value)
 return out
def pearson(xs,ys):
 mx,my=mean(xs),mean(ys);num=sum((x-mx)*(y-my) for x,y in zip(xs,ys));den=(sum((x-mx)**2 for x in xs)*sum((y-my)**2 for y in ys))**.5
 return round2(num/den) if den else 0
def result(summary,title,data):return {"summary":summary,"chart":{"title":title,"data":data}}
def svg_bar(title,data):
 items=list(data.items());width,height=900,520;left,bottom,top=110,80,70;plot_h=height-bottom-top;max_v=max([float(v) for _,v in items] or [1]);bar_w=max(24,(width-left-50)/max(len(items),1)*.62);gap=(width-left-50)/max(len(items),1)
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#081426"/><text x="{left}" y="38" fill="#fff" font-family="Arial" font-size="24" font-weight="700">{title}</text>']
 for i,(label,value) in enumerate(items):
  value=float(value);h=0 if max_v==0 else value/max_v*plot_h;x=left+i*gap;y=top+plot_h-h
  parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="5" fill="#4f9cff"/><text x="{x+bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" fill="#dcecff" font-family="Arial" font-size="13">{value:.2f}</text><text x="{x+bar_w/2:.1f}" y="{height-45}" text-anchor="middle" fill="#b8c8dd" font-family="Arial" font-size="12">{str(label)[:16]}</text>')
 parts.append('</svg>');return "".join(parts)
