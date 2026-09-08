-- Salary Benchmark SQL
-- Import ../../datasets/hr_employees.csv as table `hr_employees` before running.

SELECT employee_id,department,monthly_salary,ROUND(AVG(monthly_salary) OVER(PARTITION BY department),0) dept_avg,ROUND(monthly_salary-AVG(monthly_salary) OVER(PARTITION BY department),0) salary_gap,PERCENT_RANK() OVER(PARTITION BY department ORDER BY monthly_salary) salary_percentile,performance FROM hr_employees ORDER BY department,salary_percentile DESC;
