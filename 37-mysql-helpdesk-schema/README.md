# MySQL Helpdesk Database

A normalized MySQL 8 database design for customers, support agents, tickets, messages, tags, and service-level reporting.

## Why this belongs in my portfolio

This project connects directly to the skills and practical experience listed in my CV.

## Features

- Foreign keys, constraints, indexes, and audit timestamps
- Many-to-many ticket tagging
- SLA and agent-performance views
- Documented analytical queries

## Skills demonstrated

MySQL, database design, customer support, SQL analytics

## Run

    mysql -u root -p your_database < schema.sql
    python validate_schema.py

## Project structure

- schema.sql
- queries.sql
- validate_schema.py

All included sample data is synthetic and safe to publish.
