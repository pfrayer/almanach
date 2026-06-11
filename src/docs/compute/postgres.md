---
description: "PostgreSQL psql cheatsheet: connect, meta-commands, users, tables, CRUD, indexes, dump/restore and JSON support."
---

# PostgreSQL

## Connect

```shell
psql -U postgres                           # local superuser
psql -U user -d mydb                       # specific user + database
psql -h host -p 5432 -U user -d mydb       # remote
psql "postgresql://user:pass@host:5432/db" # connection string

# Inside psql
\q              quit
\?              help for psql commands
\h SELECT       help for SQL command
```

---

## psql meta-commands

```
\l              list databases
\c mydb         switch database
\dt             list tables in current schema
\dt *.*         list all tables in all schemas
\d tablename    describe table (columns, indexes, constraints)
\di             list indexes
\dv             list views
\df             list functions
\dn             list schemas
\du             list roles/users
\timing         toggle query timing
\x              toggle expanded display (one field per line, easier to read wide rows)
\e              open editor for current query
\i file.sql     execute SQL file
\copy           import/export (client-side)
```

---

## Databases & schemas

```sql
CREATE DATABASE mydb;
DROP DATABASE mydb;

CREATE SCHEMA myschema;
SET search_path TO myschema, public;
```

---

## Users & permissions

```sql
CREATE USER alice WITH PASSWORD 'secret';
ALTER USER alice WITH PASSWORD 'newpassword';
DROP USER alice;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mydb TO alice;
GRANT SELECT, INSERT ON TABLE mytable TO alice;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO alice;

-- Revoke
REVOKE ALL ON TABLE mytable FROM alice;

-- Make superuser
ALTER USER alice WITH SUPERUSER;
```

---

## Tables

```sql
CREATE TABLE users (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    email   TEXT UNIQUE,
    age     INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT TRUE;
ALTER TABLE users DROP COLUMN age;
ALTER TABLE users RENAME COLUMN name TO full_name;
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

DROP TABLE users;
TRUNCATE TABLE users;                       -- delete all rows, keep table
```

---

## CRUD

```sql
-- Insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')
    ON CONFLICT (email) DO NOTHING;
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')
    ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- Select
SELECT * FROM users;
SELECT name, email FROM users WHERE active = TRUE ORDER BY name LIMIT 10;
SELECT COUNT(*), age FROM users GROUP BY age HAVING COUNT(*) > 1;

-- Update
UPDATE users SET active = FALSE WHERE email = 'alice@example.com';

-- Delete
DELETE FROM users WHERE active = FALSE;
```

---

## Indexes

```sql
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_name_lower ON users(LOWER(name));   -- expression index
CREATE INDEX CONCURRENTLY idx_users_active ON users(active);  -- no table lock

DROP INDEX idx_users_email;

-- Check index usage
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
```

---

## Useful queries

```sql
-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Database size
SELECT pg_size_pretty(pg_database_size('mydb'));

-- Running queries
SELECT pid, now() - query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Kill a query
SELECT pg_cancel_backend(pid);   -- graceful
SELECT pg_terminate_backend(pid); -- force

-- Locks
SELECT * FROM pg_locks JOIN pg_stat_activity USING (pid)
WHERE NOT granted;

-- Last vacuum / analyze
SELECT relname, last_vacuum, last_analyze
FROM pg_stat_user_tables;
```

---

## Import & export

```shell
# Dump a database
pg_dump -U user mydb > mydb.sql
pg_dump -U user -Fc mydb > mydb.dump    # custom format (faster, smaller)

# Dump a single table
pg_dump -U user -t tablename mydb > table.sql

# Restore
psql -U user mydb < mydb.sql
pg_restore -U user -d mydb mydb.dump

# Copy to/from CSV
\copy users TO 'users.csv' CSV HEADER
\copy users FROM 'users.csv' CSV HEADER

# SQL equivalent (server-side path)
COPY users TO '/tmp/users.csv' CSV HEADER;
COPY users FROM '/tmp/users.csv' CSV HEADER;
```

---

## JSON support

```sql
-- JSONB column (indexed, preferred over JSON)
CREATE TABLE events (
    id   SERIAL PRIMARY KEY,
    data JSONB
);

INSERT INTO events (data) VALUES ('{"type": "click", "user": 42}');

-- Query JSONB fields
SELECT data->>'type' FROM events;
SELECT data->'user' FROM events WHERE data->>'type' = 'click';

-- Index a JSONB field
CREATE INDEX idx_events_type ON events ((data->>'type'));
```
