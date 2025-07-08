## Organizer API
## Содержание
1) [Описание](#Описание)
2) [Требования](#Требования)
3) [Установка](#Установка)
4) [Конфигурация](#Конфигурация) 
5) [Запуск](#Запуск)
6) [API](#API)
7) [Примеры запросов](#Примеры-запросов)
8) [Контакты](#Контакты)

# Описание
В основе этого сервиса лежит библиотека FastAPI на языке Python и PostgreSQL в качестве базы данных.
Сервис служит для взаимодействия с базой данных клиентов и мероприятий(добавление/удаление/поиск)

# Требования
- Python ≥ 3.13
- PostgreSQL ≥ 17.5
- Docker (опционально)

# Установка
```bash
git clone https://github.com/KarbonST/organizerAPI.git
cd organizerAPI
pip install -r requirements.txt
```
# Конфигурация
1. Создайте в корне проекта файл `.env` (рядом с `requirements.txt`, `Dockerfile` и т.д.).
2. Добавьте в него следующие переменные (пример):

   ```dotenv
   # Имя пользователя в вашей БД
   POSTGRES_USER = user_name
   # Пароль от вашей БД
   POSTGRES_PASSWORD = secret_password
   # Имя вашей БД в системе
   POSTGRES_DB = db_name
   # URL подключения к вашей базе PostgreSQL
   # Формат: dialect+driver://username:password@host:port/database (при развертывании в Docker вместо localhost использовать db)
   DATABASE_URL=postgresql://postgres:secret_password@localhost:5432/organizer_db
   ```
# Запуск
Без Docker:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Если у вас установлен Docker:
```bash
docker-compose up --build
```

# API
Эндпоинты

| Метод | Путь                                 | Описание                                  |
| :---: | :----------------------------------- | :---------------------------------------- |
| **GET**    | `/clients`                          | Получить список всех клиентов             |
| **GET**    | `/events`                           | Получить список всех мероприятий          |
| **GET**    | `/events/number_inn/{event_number}/clients/{inn}`                           | Получить клиента по номеру мероприятия и его ИНН          |
| **POST**   | `/clients`                          | Создать нового клиента                    |
| **POST**   | `/events`                           | Создать новое мероприятие                 |
| **DELETE** | `/events`                | Удалить все мероприятия (и всех клиентов с них)     |
| **DELETE** | `/events/number_inn/{event_number}/clients/{inn}` | Удалить клиента с мероприятия с заданным ИНН              |
| **DELETE** | `/events/event_number/{event_number}`                | Удалить мероприятие (и всех его клиентов) по его номеру     |
| **DELETE** | `/events/name/{event_name}`                | Удалить мероприятие (и всех его клиентов) по его наименованию     |

# Примеры запросов
```bash
curl -X 'POST' \
  'https://localhost:8000/clients' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_fullname": "Иванов И.И.",
  "inn": "3453625174812",
  "company_name": "ООО Ромашка",
  "is_client": "да",
  "working_sphere": "Флористика",
  "contact_fullname": "Петров П.П.",
  "phone": "+7 (999) 743-42-45",
  "client_request": "Подключение торгового эквайринга",
  "event_number": 1
}'
```

```bash
curl -X 'POST' \
  'https://localhost:8000/events' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Новый год"
}'
```
# Контакты
- email: mikhailbykadorov@mail.ru
- tg: @KarbonST
