# UFOffice

## Backend

### 1. Настройка

> .env

```
PYTHON_AD=C:/Users/

DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=ufoffice

HOST=127.0.0.1
PORT=8000
```

>  **Необходим Python версии 3.9 и выше**

Настройка директории и установка зависимостей

```ps
python -m venv env
env/scripts/activate
pip install -r requirements.txt
```

### 2. Запуск 
```console
uvicorn main:app
```
