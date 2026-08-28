#!/usr/bin/env python3
"""Port Scan Report Parser - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import xml.etree.ElementTree as ET
    root=ET.fromstring(data["nmap_xml"]);hosts=[]
    for host in root.findall("host"):
     addr=host.find("address").attrib.get("addr","unknown");ports=[]
     for port in host.findall("./ports/port"):
      state=port.find("state").attrib.get("state");service=port.find("service");ports.append({"port":int(port.attrib["portid"]),"protocol":port.attrib["protocol"],"state":state,"service":service.attrib.get("name") if service is not None else "unknown"})
     hosts.append({"address":addr,"open_ports":[p for p in ports if p["state"]=="open"]})
    return {"hosts":hosts,"source":"pre-existing authorized report","active_scan_performed":False}

def main()->None:
 parser=argparse.ArgumentParser(description='Port Scan Report Parser')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
