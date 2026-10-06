# AnalystBench

AnalystBench is a project for testing whether an autonomous AI data analyst can be trusted to answer realistic business questions correctly and support its conclusions with evidence.

The project will combine:
- PostgreSQL and SQL
- Python
- AI model/tool use
- evaluation engineering
- reliability testing
- benchmark-driven analysis

## Database Setup

Create the PostgreSQL database:

```bash
createdb analystbench
```

Create the database tables:

```bash
psql analystbench -f schema.sql
```

Load the synthetic seed data:

```bash
psql analystbench -f seed_data.sql
```

Connect to the database:

```bash
psql analystbench
```

Inspect the available tables:

```text
\dt
```
