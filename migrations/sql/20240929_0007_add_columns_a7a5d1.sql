ALTER TABLE accounts.promotions ADD COLUMN IF NOT EXISTS short_description VARCHAR(255) NULL;
ALTER TABLE accounts.promotions ADD COLUMN IF NOT EXISTS start_date DATE NULL;
ALTER TABLE accounts.promotions ADD COLUMN IF NOT EXISTS end_date DATE NULL;
