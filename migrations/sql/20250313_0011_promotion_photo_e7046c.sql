ALTER TABLE accounts.promotions DROP COLUMN photo;
ALTER TABLE accounts.promotions ADD COLUMN IF NOT EXISTS photo_name VARCHAR(255) NULL;
