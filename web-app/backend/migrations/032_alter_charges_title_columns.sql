-- 032_alter_charges_title_columns.sql
-- เปลี่ยนชนิดข้อมูลคอลัมน์ title_th/title_en ให้รองรับข้อความยาว

ALTER TABLE charges
  ALTER COLUMN title_th TYPE TEXT,
  ALTER COLUMN title_en TYPE TEXT;

