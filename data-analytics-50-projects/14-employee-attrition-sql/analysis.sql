-- Employee Attrition SQL
-- Import ../../datasets/hr_employees.csv as table `hr_employees` before running.

SELECT department, COUNT(*) headcount, SUM(attrition) exits, ROUND(100.0*AVG(attrition),1) attrition_pct, ROUND(AVG(monthly_salary),0) avg_salary FROM hr_employees GROUP BY department ORDER BY attrition_pct DESC;
