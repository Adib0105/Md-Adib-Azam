# Payroll Database

A MySQL 8 relational mini-project with two domain tables, referential integrity, validation, synthetic sample data, indexes and an analytical view.

## Run

    mysql -u USER -p DATABASE < 01-schema.sql
    mysql -u USER -p DATABASE < 02-sample-data.sql
    mysql -u USER -p DATABASE < 03-analytics-queries.sql

Metric: **net pay (INR)**. Use a disposable development database for the sample.
