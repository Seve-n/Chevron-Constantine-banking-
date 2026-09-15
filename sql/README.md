# SQL Analysis: Setup

The queries in this folder run against a local SQLite database built from
`data/processed/banking_customer_journeys_clean.csv`. SQLite was chosen over a full database
server (PostgreSQL, MySQL) because it needs zero setup (the whole database is a single file),
which matters for a portfolio project someone else will clone and try to run.

## Loading the CSV into SQLite

**Option A: Python** (recommended, already used throughout this project)

```bash
python sql/load_to_sqlite.py
```

This reads the processed CSV with pandas and writes it into `sql/novabank.db` as a table named
`journeys`, using `DataFrame.to_sql()`. The `.db` file is not committed to git (see
`.gitignore`): it's a disposable build artifact, regenerated from the CSV in one command.

**Option B: the `sqlite3` command-line tool**, if you prefer not to involve Python at all

```bash
sqlite3 sql/novabank.db
sqlite> .mode csv
sqlite> .import --skip 1 data/processed/banking_customer_journeys_clean.csv journeys
```

(`--skip 1` skips the header row; it requires a reasonably recent `sqlite3` version. On an
older version, import the header as data and delete that one row afterward.)

## Running the queries

Once `sql/novabank.db` exists, open it with the `sqlite3` CLI, or any GUI tool (e.g.
[DB Browser for SQLite](https://sqlitebrowser.org/)), and run the `.sql` files in this folder:

- `01_basic_kpis.sql`: overall completion/abandonment rate, durations, error rate, support
  contact rate.
- `02_funnel_analysis.sql`: step-by-step funnel and drop-off rate per journey.
- `03_customer_segments.sql`: abandonment rate by customer segment, age group, device, and
  channel.

Each file is a sequence of independent `SELECT` statements. Copy-paste and run them one at a
time, or run the whole file if your tool supports multiple statements.
