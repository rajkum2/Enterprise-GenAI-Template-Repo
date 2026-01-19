CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  email TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS roles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_roles (
  user_id TEXT NOT NULL REFERENCES users(id),
  role_id TEXT NOT NULL REFERENCES roles(id),
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  PRIMARY KEY (user_id, role_id, tenant_id)
);

CREATE TABLE IF NOT EXISTS documents (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  source_uri TEXT NOT NULL,
  title TEXT,
  acl JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chunks (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL REFERENCES documents(id),
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  content TEXT NOT NULL,
  embedding JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS task_runs (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  status TEXT NOT NULL,
  input JSONB NOT NULL,
  output JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS steps (
  id TEXT PRIMARY KEY,
  task_run_id TEXT NOT NULL REFERENCES task_runs(id),
  name TEXT NOT NULL,
  status TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tool_invocations (
  id TEXT PRIMARY KEY,
  task_run_id TEXT NOT NULL REFERENCES task_runs(id),
  tool_name TEXT NOT NULL,
  request JSONB NOT NULL,
  response JSONB,
  status TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS approvals (
  id TEXT PRIMARY KEY,
  task_run_id TEXT NOT NULL REFERENCES task_runs(id),
  status TEXT NOT NULL,
  approved_by TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  key TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  response JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE (tenant_id, key)
);
