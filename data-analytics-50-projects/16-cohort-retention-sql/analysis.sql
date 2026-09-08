-- Customer Cohort SQL
-- Import ../../datasets/customers.csv as table `customers` before running.

SELECT substr(signup_date,1,7) cohort, COUNT(*) customers, ROUND(100.0*(1-AVG(churned)),1) retention_pct, ROUND(AVG(monthly_spend),0) avg_spend FROM customers GROUP BY cohort ORDER BY cohort;
