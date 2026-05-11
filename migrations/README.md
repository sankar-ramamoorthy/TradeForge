# Runtime Database Migrations

Alembic migrations manage physical Postgres schema for the runtime
infrastructure layer.

Migrations do not define semantic truth. Event meaning, lifecycle authority,
workspace semantics, persona interpretation, and replay behavior remain governed
by the knowledge base and runtime ADRs.

The initial bootstrap revision intentionally creates no domain tables. Event
ledger schema belongs to TF-0026, and projection persistence belongs to its own
scoped work.
