🌐 Лабораторная работа — Настройка двух приложений с Nginx и Uvicorn

## 📖 Описание проекта
В этой работе были созданы два независимых веб-приложения (Project 1 и Project 2), запущенные через `Uvicorn` и объединённые под одним прокси-сервером `Nginx`.  
Каждое приложение работает на своём порту, а Nginx направляет трафик по доменным именам `project1.local` и `project2.local`.

---

## ⚙️ Структура проекта

web_projects/
├── project1/
│ └── app1.py
├── project2/
│ └── app2.py
├── nginx/
│ ├── project1.conf
│ └── project2.conf
└── README.md

## 🧩 Шаг 1 — Создание виртуального окружения
```bash
python3 -m venv .venv
source .venv/bin/activate
```

📦 Шаг 2 — Установка зависимостей

```pip install "uvicorn[standard]" starlette```

💻 Шаг 3 — Код приложений
```project1/app1.py```

```
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request):
    return JSONResponse({'message': 'Hello from Project 1!'})

project2/app2.py

from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request):
    return JSONResponse({'message': 'Hello from Project 2!'})
```

🚀 Шаг 4 — Запуск серверов Uvicorn

# Project 1
```uvicorn app1:app --host 127.0.0.1 --port 8001```

# Project 2
```uvicorn app2:app --host 127.0.0.1 --port 8002```

Проверка в браузере:

    http://127.0.0.1:8001

→ Project 1

http://127.0.0.1:8002

    → Project 2

🧱 Шаг 5 — Настройка Nginx

Созданы два конфигурационных файла в каталоге /etc/nginx/sites-available/.
nginx/project1.conf

```
server {
    listen 80;
    server_name project1.local;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
nginx/project2.conf
```
server {
    listen 80;
    server_name project2.local;

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

🧾 Шаг 6 — Проверка конфигурации Nginx

```
sudo nginx -t
sudo systemctl restart nginx
```

🌍 Шаг 7 — Настройка локальных доменов

Добавьте в файл /etc/hosts:

```
127.0.0.1   project1.local
127.0.0.1   project2.local
```

После этого можно открыть:

    http://project1.local

    http://project2.local
