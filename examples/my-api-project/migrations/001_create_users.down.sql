-- Migration: Rollback users table
-- Version: 001
-- Description: Remove user table and related objects

-- Drop trigger first (depends on function)
DROP TRIGGER IF EXISTS update_users_updated_at ON users;

-- Drop function
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Drop index
DROP INDEX IF EXISTS idx_users_email;

-- Drop table
DROP TABLE IF EXISTS users;
