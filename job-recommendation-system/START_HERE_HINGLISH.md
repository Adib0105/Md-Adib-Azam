# Job Recommendation System — Kaise chalana hai

1. GitHub repo ko **Code → Download ZIP** se download karke **Extract All** karo, ya repo clone karo.
2. VS Code mein `job-recommendation-system` wala folder kholo. Isi folder mein `app.py` dikhna chahiye.
3. **Terminal → New Terminal** kholo.

   Agar terminal `Md-Adib-Azam` repo ke root mein hai, pehle `cd job-recommendation-system` chalao.
4. Python **3.11 ya 3.12, 64-bit** installed hona chahiye.
5. Ye commands ek-ek karke paste karo:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe scripts\seed_database.py --demo
.\venv\Scripts\python.exe app.py
```

6. Chrome kholo aur address bar mein ye likho:

**http://127.0.0.1:5000**

Terminal khula rehne do. Band karne ke liye **Ctrl+C**.

## Demo login

Candidate:

- Email: `demo@jobmatch.com`
- Password: `Demo@123`

Admin ke liye `/admin/login` kholo:

- Email: `admin@jobmatch.com`
- Password: `Admin@123`

Ye sirf local demo passwords hain. Apna account banana ho to **Get started** dabao.

## Project ka demo kaise dena hai

1. Profile mein education, experience aur skills bharo. Fresher ho to experience **0** likho.
2. Salary saal ki bharo: **5 LPA = 500000**.
3. Resume PDF/DOCX upload karo. Extracted details check karke confirm karo.
4. Recommendations kholo. Job details mein score ka reason aur missing skills dikhenge.
5. Job save karo aur **Apply · Track locally** dabao. Application tracker mein status update karo.
6. Career Insights se charts dikhao.
7. Skill Analysis mein learning gaps dekho.
8. Career Simulator mein Tableau/DAX jaisi skill add karke before/after estimated score compare karo.
9. Match History mein profile updates ka difference dekho.
10. Logout karke Admin login se job add/edit/remove dikhao.

## Dhyan rahe

- Ye **local web project** hai, phone app ya desktop executable nahi.
- Internet dependencies install karne ke liye chahiye; uske baad core project offline chalta hai.
- Manrope aur Fraunces fonts project ke andar hain. Cards, hero illustration aur charts mein smooth animations hain; device par reduced motion on ho to decorative animation band ho jayega.
- `localhost` link tumhare computer par server chalne ke baad khulega. GitHub ka repository link website ka live link nahi hota.
- 640 jobs aur company details demo data hain. Apply dabane par employer ko kuch send nahi hota.
- Score actual algorithm se calculate hota hai. Lekin job milne ka guarantee/percentage chance nahi hai.
- Agli baar sirf `.\venv\Scripts\python.exe app.py` chalana hai.
- Pura technical explanation aur troubleshooting `README.md` mein hai.
