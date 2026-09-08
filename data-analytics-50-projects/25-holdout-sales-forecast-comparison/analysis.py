"""Does seasonal naive beat a three-month mean on the last 12 months?"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run import run_one
if __name__ == "__main__": run_one(25)
