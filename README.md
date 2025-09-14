# hrsdesk
hrsdesk.ru
## Работа с базой данных (PostgreSQL)

### Требования
- Docker Desktop
- Контейнер PostgreSQL, запущенный через `docker-compose up -d`
- Установленный клиент `psql` (идёт в комплекте с Docker-образом Postgres или можно поставить отдельно)

### Подключение к БД
```bash
psql -h localhost -U hrs -d hrsdesk

Создать структуру (схему таблиц):
psql -h localhost -U hrs -d hrsdesk -f db/schema.sql

Загрузить тестовые данные:
psql -h localhost -U hrs -d hrsdesk -f db/data.sql


Очистить базу (удалить все таблицы):
psql -h localhost -U hrs -d hrsdesk -f db/drop.sql

