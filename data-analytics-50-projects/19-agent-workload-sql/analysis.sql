-- Support Agent Workload SQL
-- Import ../../datasets/support_tickets.csv as table `support_tickets` before running.

SELECT agent,COUNT(*) assigned,SUM(CASE WHEN status='Open' THEN 1 ELSE 0 END) open_tickets,ROUND(100.0*AVG(CASE WHEN status='Closed' THEN 1.0 ELSE 0 END),1) closure_pct,ROUND(AVG(first_response_min),1) avg_response FROM support_tickets GROUP BY agent ORDER BY assigned DESC;
