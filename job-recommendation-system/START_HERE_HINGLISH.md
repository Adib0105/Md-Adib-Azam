# JobMatch — shuru kaise karein

Repo download/clone karke **job-recommendation-system** folder VS Code mein kholo. Python 3.11 ya 3.12 (64-bit) chahiye.

PowerShell terminal mein:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe scripts\seed_database.py
.\venv\Scripts\python.exe scripts\create_admin.py
.\venv\Scripts\python.exe app.py
```

Chrome mein **http://127.0.0.1:5000** kholo. Terminal chalta rehna chahiye. Band karne ke liye Ctrl+C.

- User account: **Create account** se banao; login `/login` par.
- Admin: setup command mein apna email aur private password do; login `/admin/login` par. Koi fixed/public admin password nahi hai.
- Purana demo admin ho to `python scripts/create_admin.py --reset-existing` se naya private password set karo.
- Optional demo user: `python scripts/seed_database.py --demo`; naya random candidate password terminal mein ek baar milega.
- APIs ke bina 640 demo jobs, profile, resume review, recommendations, charts aur tracker chalenge.
- Real jobs ke liye Adzuna keys environment mein set karo; optional USAJOBS credentials bhi support hote hain. Admin → Providers → Enable/Test/Sync. `.env.example` sirf reference hai, auto-load nahi hoti.
- Forgot password development mein private `instance/mail/` folder ki newest `.eml` file mein link deta hai. Production mein SMTP configure karna hoga. Link 30 minute valid aur single-use hai.
- Alerts ke liye scheduler/Task Scheduler se `python scripts/process_alerts.py` run karna hoga. Email alerts se pehle Account settings mein email verify karo.
- Purane app ka data ho to processes stop karke backup lo, phir `python scripts/upgrade_database.py` chalao. Existing records preserve honge.

Baad mein start karne ke liye sirf `venv\Scripts\python.exe app.py` ya `start_windows.cmd`.

Demo jobs fictional hain. Real jobs par **Apply on source** original website kholta hai; **Add to tracker** sirf apni progress save karta hai. Score hiring ya ATS guarantee nahi hai.

Details: [README](README.md) · [Upgrade report](docs/UPGRADE_REPORT.md).
