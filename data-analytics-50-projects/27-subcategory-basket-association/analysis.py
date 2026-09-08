"""Which subcategory pairs co-occur in at least 20 orders, and with what lift?"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run import run_one
if __name__ == "__main__": run_one(27)
