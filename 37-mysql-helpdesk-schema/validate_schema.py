from pathlib import Path

schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8").lower()
queries = Path(__file__).with_name("queries.sql").read_text(encoding="utf-8").lower()
required_tables = ["customers", "agents", "tickets", "ticket_messages", "tags", "ticket_tags"]
for table in required_tables:
    assert f"create table {table}" in schema
assert schema.count("foreign key") >= 5
assert "create view ticket_sla_status" in schema
assert "create view agent_performance" in schema
assert "group by" in queries and "order by" in queries
print("MySQL helpdesk schema validation passed")
