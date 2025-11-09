🌐 **Лабораторная работа — Настройка двух приложений с Nginx и Uvicorn (HTTPS)**

📖 **Описание проекта**  
В этой работе были созданы два независимых веб-приложения (Project 1 и Project 2), запущенные через Uvicorn и объединённые под одним прокси-сервером Nginx с поддержкой HTTPS.  
Каждое приложение работает на своём порту, а Nginx направляет трафик по доменным именам `project1.local` и `project2.local`.

⚙️ **Структура проекта**
web_projects/
 ├── project1/
 │ └── app1.py
 ├── project2/
 │ └── app2.py
 ├── nginx/
 │ ├── project1.conf
 │ └── project2.conf
 └── README.md


---

 **Шаг 1 — Создание виртуального окружения**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
<img width="426" height="51" alt="image" src="https://github.com/user-attachments/assets/24e95f77-2845-42fa-b1bf-bbeb53976ee2" />


**Шаг 2 — Установка зависимостей**
```bash
pip install "uvicorn[standard]" starlette
```
<img width="502" height="274" alt="image" src="https://github.com/user-attachments/assets/0420f239-3aac-4b29-a8e1-56d6a3297bb1" />


 Шаг 2.1 — Создание собственного SSL-сертификата (self-signed)

Для HTTPS нужно сгенерировать самоподписанный сертификат:

```bash
mkdir -p ~/projects/web_projects/nginx/certs
cd ~/projects/web_projects/nginx/certs
```
<img width="721" height="605" alt="image" src="https://github.com/user-attachments/assets/e45add70-f71c-497a-8d2d-3af1ccfc7ea1" />


 **Шаг 3 — Код приложений**

project1/app1.py

python
```bash
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request):
    return JSONResponse({'message': 'Hello from Project 1!'})
```
project2/app2.py

python
```bash
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request):
    return JSONResponse({'message': 'Hello from Project 2!'})
```

 **Шаг 4 — Запуск серверов Uvicorn**

Terminal 1 (Project 1):

```bash
cd ~/projects/web_projects/project1
uvicorn app1:app --host 127.0.0.1 --port 8001
```
<img width="605" height="124" alt="image" src="https://github.com/user-attachments/assets/e1311d3f-be42-4222-b071-75be1986dd03" />
<img width="957" height="932" alt="image" src="https://github.com/user-attachments/assets/cdda05ae-4b87-474e-9333-5b1483e5194d" />



Terminal 2 (Project 2):

```bash
cd ~/projects/web_projects/project2
uvicorn app2:app --host 127.0.0.1 --port 8002
```
<img width="637" height="106" alt="image" src="https://github.com/user-attachments/assets/e48dd36f-65fd-448d-b00e-9414611fed14" />
<img width="958" height="933" alt="image" src="https://github.com/user-attachments/assets/da64fd7d-e4e3-4242-a259-911521a6a90a" />


 **Шаг 5 — Настройка Nginx с HTTPS**

nginx/project1.conf

nginx
```bash
server {
    listen 443 ssl;
    server_name project1.local;

    ssl_certificate /home/kali/projects/web_projects/nginx/certs/fullchain.pem;
    ssl_certificate_key /home/kali/projects/web_projects/nginx/certs/privkey.pem;

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

nginx
```bash
server {
    listen 443 ssl;
    server_name project2.local;

    ssl_certificate /home/kali/projects/web_projects/nginx/certs/fullchain.pem;
    ssl_certificate_key /home/kali/projects/web_projects/nginx/certs/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

 **Шаг 6 — Проверка конфигурации Nginx**

bash
Copy code
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx

<img width="674" height="159" alt="image" src="https://github.com/user-attachments/assets/4b7f0ccc-41e8-4569-9cfe-4f99516f6255" />


 **Шаг 7 — Настройка локальных доменов**

Добавьте в файл /etc/hosts:

```bash
127.0.0.1   project1.local
127.0.0.1   project2.local
```

<img width="564" height="203" alt="image" src="https://github.com/user-attachments/assets/276b5a28-59b0-4fee-ae66-bbb79239f019" />


 **Шаг 8 — Тестирование HTTPS через браузер**

https://project1.local → Project 1
https://project2.local → Project 2

<img width="408" height="87" alt="image" src="https://github.com/user-attachments/assets/f2541147-0b92-47d0-8ce0-dfaa1a96b929" />


Примечание: Поскольку сертификат самоподписанный, нужно нажать “Advanced → Proceed anyway” в браузере.
