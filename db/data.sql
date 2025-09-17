-- =======================================
-- DEMO DATA FOR HRS DESK PROJECT
-- =======================================

-- 1. Продукты
INSERT INTO products (code, name, description) VALUES
  ('OPERA', 'PMS Oracle Opera', 'Основная система управления отелем'),
  ('SIMPHONY', 'POS Simphony', 'Система для ресторанов отелей'),
  ('TNG', 'TNG Loyalty & SPA', 'Система лояльности, SPA и проката');

-- 2. Отель
INSERT INTO properties (code, name, address, timezone) VALUES
  ('MARRIMP', 'Marriott Imperial Plaza',
   'Краснопрудная ул., 12, Москва, Россия', 'Europe/Moscow');

-- 3. Связь отеля с продуктами (отель id=1 → все продукты)
INSERT INTO property_products (property_id, product_id) VALUES
  (1, 1), (1, 2), (1, 3);

-- 4. Сотрудник отеля (ИТ-менеджер Иванов)
-- Пароль: Password123
INSERT INTO property_employees (property_id, first_name, last_name, email, password_hash, phone, role_in_property) VALUES
  (1, 'Иван', 'Иванов', 'iivanov@marriott.ru',
   '$2b$12$KIX5B7zR8BZ48z8KyWjOueJqzQINbAOl0zRkNeMt4wPcOEHl7Y3lG',
   '+7-999-123-45-67', 'IT Manager');

-- 5. Сотрудники HRS
-- 5.1 Админ HRS
INSERT INTO hrs_employees (first_name, last_name, email, password_hash, phone, is_admin, job_title, product_id) VALUES
  ('Admin', 'HRS', 'admin@hrsdesk.ru',
   '$2b$12$KIX5B7zR8BZ48z8KyWjOueJqzQINbAOl0zRkNeMt4wPcOEHl7Y3lG',
   '+7-495-000-00-00', TRUE, 'System Administrator', NULL);

-- 5.2 Специалист по Opera (продукт id=1)
INSERT INTO hrs_employees (first_name, last_name, email, password_hash, phone, is_admin, job_title, product_id) VALUES
  ('Максим', 'Руднев', 'mrudnev@hrsdesk.ru',
   '$2b$12$KIX5B7zR8BZ48z8KyWjOueJqzQINbAOl0zRkNeMt4wPcOEHl7Y3lG',
   '+7-910-777-88-99', FALSE, 'Leading Opera Specialist', 1);

-- 6. Уровни поддержки (L1, L2, L3)
INSERT INTO support_levels (code, description) VALUES
  ('L1', 'Первая линия поддержки'),
  ('L2', 'Вторая линия поддержки'),
  ('L3', 'Разработка и R&D');
