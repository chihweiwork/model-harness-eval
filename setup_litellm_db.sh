#!/usr/bin/env bash
# Setup LiteLLM database in PostgreSQL
# Run this script manually: sudo bash setup_litellm_db.sh

set -euo pipefail

echo "Creating LiteLLM database and user..."

sudo -u postgres psql <<EOF
-- Create user if not exists
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'litellm') THEN
    CREATE USER litellm WITH PASSWORD 'litellm_password';
    RAISE NOTICE 'User litellm created';
  ELSE
    RAISE NOTICE 'User litellm already exists';
  END IF;
END
\$\$;

-- Create database if not exists
SELECT 'CREATE DATABASE litellm OWNER litellm'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'litellm')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE litellm TO litellm;

-- Display results
\echo '=== Database ==='
\l litellm

\echo '=== User ==='
\du litellm
EOF

echo ""
echo "✓ Database setup complete!"
echo ""
echo "Connection string:"
echo "  postgresql://litellm:litellm_password@localhost:5432/litellm"
