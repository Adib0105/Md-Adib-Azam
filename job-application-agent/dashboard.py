import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
DB = ROOT / "jobs.db"

st.set_page_config(page_title="Job Application Agent", layout="wide")
st.title("WFH Job Application Agent")
st.caption("Truth-first matching: verified remote jobs, no invented answers, duplicate protection.")

if not DB.exists():
    st.info("No jobs found yet. Run agent.py first.")
    st.stop()

con = sqlite3.connect(DB)
df = pd.read_sql_query("SELECT * FROM jobs ORDER BY discovered_at DESC", con)
con.close()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Found", len(df))
c2.metric("Qualified", int((df.verdict == "QUALIFIED").sum()))
c3.metric("Applied", int((df.status == "APPLIED").sum()))
c4.metric("Needs review", int((df.verdict == "REVIEW").sum()))

status = st.multiselect("Verdict", ["QUALIFIED", "REVIEW", "SKIP"], default=["QUALIFIED", "REVIEW"])
view = df[df.verdict.isin(status)] if status else df
st.dataframe(view[["company","title","score","verdict","status","reason","url"]], use_container_width=True, hide_index=True,
             column_config={"url": st.column_config.LinkColumn("Application")})
