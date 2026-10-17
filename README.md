# TaskFlow

Минимальное веб-приложение списка задач: React + TypeScript, FastAPI, PostgreSQL, SQLAlchemy и Alembic.

## Запуск

1. Установите Docker Desktop, Python 3.12+ и Node.js LTS.
2. В корне проекта выполните:

```powershell
docker compose up -d
cd backend
python -m pip install -e ".[dev]"
python -m alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

3. В другом терминале:

```powershell
cd frontend
npm install
npm run dev
```

Откройте адрес, который покажет Vite (обычно `http://localhost:5173`). Frontend обращается к Backend через Vite-прокси `/api`.

## Проверка

```powershell
cd backend
python -m pytest
```

Миграции выполняются вручную перед запуском Backend и после изменения модели. `docker compose down -v` удаляет том PostgreSQL и все задачи.
