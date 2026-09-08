-- Support Ticket SLA SQL
-- Import ../../datasets/support_tickets.csv as table `support_tickets` before running.

SELECT agent, channel, COUNT(*) tickets, ROUND(AVG(first_response_min),1) avg_response_min, ROUND(100.0*AVG(CASE WHEN first_response_min>30 THEN 1.0 ELSE 0 END),1) breach_pct, ROUND(AVG(csat),2) avg_csat FROM support_tickets GROUP BY agent,channel ORDER BY breach_pct DESC;
