# MySQL Helpdesk Database

A normalized MySQL 8 design for customer-support tickets, conversations, tagging and SLA reporting.

## Data model

| Table | Purpose |
|---|---|
| `customers` | Customer identity and unique email |
| `agents` | Support staff, team and active status |
| `tickets` | Priority, status, ownership and SLA timestamps |
| `ticket_messages` | Time-ordered customer, agent and system messages |
| `tags` | Reusable classification labels |
| `ticket_tags` | Many-to-many ticket classification |

## Design decisions

- Foreign keys protect customer, agent, message and tag relationships.
- Cascading cleanup removes dependent messages and tag links with a ticket.
- A check constraint prevents resolution timestamps before opening time.
- Queue and agent indexes support common operational filters.
- `ticket_sla_status` and `agent_performance` views centralize reporting logic.

## Run and verify

```bash
mysql -u root -p your_database < schema.sql
python validate_schema.py
```

The static validator checks six required tables, at least five foreign keys, both reporting views and analytical grouping/sorting queries.

## Files

- `schema.sql` — tables, constraints, indexes and views
- `queries.sql` — operational and analytical examples
- `validate_schema.py` — repeatable structure checks

All included records are synthetic.

[Back to flagship case studies](../PORTFOLIO_SHOWCASE.md)
