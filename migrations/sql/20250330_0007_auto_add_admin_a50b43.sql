INSERT INTO accounts.admin (id, name, username, password_hash, status, created_at, updated_at)
SELECT
    gen_random_uuid(),
    'Главный Администратор',
    'admin',
    '$2b$12$263/60AiJZE8NnU2WHyLP.FfC6KclhTo1K2D3QkrsAdNsU5G.MA1G',
    'ACTIVE',
    NOW(),
    NOW()
WHERE NOT EXISTS (SELECT 1 FROM accounts.admin);