# JobMatch — shuru kaise karein

Python **3.11 ya 3.12 (64-bit)** chahiye. Installation mein **Add python.exe to PATH** select karo.

Windows par sabse aasaan:

1. Downloaded ZIP par **Extract All** karo.
2. Extracted folder mein **`start_windows.cmd`** par double-click karo. Standalone JobMatch ZIP mein `app.py`, `requirements.txt` aur launcher seedhe extracted folder mein milenge. Full GitHub repo download kiya ho to **`job-recommendation-system`** folder kholo.
3. Launcher apne app folder mein switch karke venv banayega, packages install karega, demo jobs taiyar karega aur app chalayega. First setup mein internet aur thoda time chahiye. Failed step par launcher rukta hai; terminal ki pehli error dekho.
4. Terminal mein **JobMatch is running** aane par Chrome mein **http://127.0.0.1:5000** kholo. Terminal khula rakho. Band karne ke liye Ctrl+C.

Agli baar bhi `start_windows.cmd` chalao. Installed packages aur existing accounts/jobs dobara use honge. Sirf setup karna ho to `setup_windows.cmd` chala sakte ho.

Manual setup ke liye VS Code/PowerShell mein **wahi folder kholo jisme `app.py` aur `requirements.txt` hain**. Agar `requirements.txt` ya `scripts\seed_database.py` not found aa raha hai to terminal wrong folder mein hai. Purane ZIP/full repo ke outer folder se `cd .\job-recommendation-system` karo.

PowerShell terminal mein:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe scripts\seed_database.py
.\venv\Scripts\python.exe app.py
```

Chrome mein **http://127.0.0.1:5000** kholo. Terminal chalta rehna chahiye. Band karne ke liye Ctrl+C.

- User account: **Create account** se banao; login `/login` par.
- Admin test karna ho to app folder mein alag PowerShell kholo aur `.\venv\Scripts\python.exe scripts\create_admin.py` chalao. Apna email aur private password do; login `/admin/login` par. Koi fixed/public admin password nahi hai.
- Purana demo admin ho to `python scripts/create_admin.py --reset-existing` se naya private password set karo.
- Optional demo user: `python scripts/seed_database.py --demo`; naya random candidate password terminal mein ek baar milega.
- APIs ke bina 640 demo jobs, profile, resume review, recommendations, charts aur tracker chalenge.
- Real jobs ke liye Adzuna keys environment mein set karo; optional USAJOBS credentials bhi support hote hain. Admin → Providers → Enable/Test/Sync. `.env.example` sirf reference hai, auto-load nahi hoti.
- Forgot password development mein private `instance/mail/` folder ki newest `.eml` file mein link deta hai. Production mein SMTP configure karna hoga. Link 30 minute valid aur single-use hai.
- Alerts ke liye scheduler/Task Scheduler se `python scripts/process_alerts.py` run karna hoga. Email alerts se pehle Account settings mein email verify karo.
- Purane app ka data ho to processes stop karke backup lo, phir `python scripts/upgrade_database.py` chalao. Existing records preserve honge.

Agar existing venv wrong Python se bana hai, app band karke `venv` ko `venv_old` rename karo, phir `start_windows.cmd` chalao. Launcher supported Python se naya environment banayega.

Demo jobs fictional hain. Real jobs par **Apply on source** original website kholta hai; **Add to tracker** sirf apni progress save karta hai. Score hiring ya ATS guarantee nahi hai.

Details: [Download guide](DOWNLOAD_RUN_GUIDE.txt) · [README](README.md) · [AI/ML report](docs/FINAL_AI_ML_REPORT.md).
