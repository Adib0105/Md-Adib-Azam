-- Open queue ordered by urgency and SLA deadline.
SELECT ticket_id, subject, priority, sla_due_at
FROM tickets
WHERE status IN ('open', 'pending')
ORDER BY FIELD(priority, 'urgent', 'high', 'normal', 'low'), sla_due_at;

-- Category mix during the last 30 days.
SELECT category, COUNT(*) AS tickets,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS share_percent
FROM tickets
WHERE opened_at >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
GROUP BY category
ORDER BY tickets DESC;

-- SLA breach rate.
SELECT
  ROUND(100 * SUM(sla_status = 'breached') / COUNT(*), 1) AS breach_rate_percent
FROM ticket_sla_status;

-- Workload by active agent.
SELECT a.full_name, COUNT(t.ticket_id) AS open_tickets
FROM agents a
LEFT JOIN tickets t
  ON t.agent_id = a.agent_id AND t.status IN ('open', 'pending')
WHERE a.active = TRUE
GROUP BY a.agent_id, a.full_name
ORDER BY open_tickets DESC;
