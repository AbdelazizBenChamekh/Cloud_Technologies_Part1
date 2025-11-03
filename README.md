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

yaml
Copy code

---

🧩 **Шаг 1 — Создание виртуального окружения**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
<img width="426" height="51" alt="image" src="https://github.com/user-attachments/assets/24e95f77-2845-42fa-b1bf-bbeb53976ee2" />


📦 Шаг 2 — Установка зависимостей
```bash
pip install "uvicorn[standard]" starlette
```
<img width="502" height="274" alt="image" src="https://github.com/user-attachments/assets/0420f239-3aac-4b29-a8e1-56d6a3297bb1" />


🔐 Шаг 2.1 — Создание собственного SSL-сертификата (self-signed)

Для HTTPS нужно сгенерировать самоподписанный сертификат:

bash
Copy code
mkdir -p ~/projects/web_projects/nginx/certs
cd ~/projects/web_projects/nginx/certs

# Генерация ключа и сертификата
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout privkey.pem \
    -out fullchain.pem \
    -subj "/C=NL/ST=SomeState/L=SomeCity/O=ITMO/OU=Lab/CN=project1.local"
privkey.pem — приватный ключ

fullchain.pem — сертификат

📸 Скриншот: step2_ssl_cert.png

Повторите для project2.local, или используйте один сертификат для обоих локальных доменов.

💻 Шаг 3 — Код приложений

project1/app1.py

python
Copy code
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request):
    return JSONResponse({'message': 'Hello from Project 1!'})
project2/app2.py

python
Copy code
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request):
    return JSONResponse({'message': 'Hello from Project 2!'})
📸 Скриншоты кода:

step3_app1_code.png

step3_app2_code.png

🚀 Шаг 4 — Запуск серверов Uvicorn

Terminal 1 (Project 1):

bash
Copy code
cd ~/projects/web_projects/project1
uvicorn app1:app --host 127.0.0.1 --port 8001
📸 Скриншот: step4_project1_uvicorn.png

Terminal 2 (Project 2):

bash
Copy code
cd ~/projects/web_projects/project2
uvicorn app2:app --host 127.0.0.1 --port 8002
📸 Скриншот: step4_project2_uvicorn.png

🧱 Шаг 5 — Настройка Nginx с HTTPS

nginx/project1.conf

nginx
Copy code
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
nginx/project2.conf

nginx
Copy code
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
📸 Скриншоты конфигов:

step5_project1_nginx.png

step5_project2_nginx.png

🧾 Шаг 6 — Проверка конфигурации Nginx

bash
Copy code
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
📸 Скриншоты проверки Nginx:

step6_nginx_test.png

step6_nginx_status.png

🌍 Шаг 7 — Настройка локальных доменов

Добавьте в файл /etc/hosts:

lua
Copy code
127.0.0.1   project1.local
127.0.0.1   project2.local
📸 Скриншот: step7_hosts.png

🌐 Шаг 8 — Тестирование HTTPS через браузер

https://project1.local → Project 1
📸 Скриншот: project1_https.png

https://project2.local → Project 2
📸 Скриншот: project2_https.png

✅ Примечание: Поскольку сертификат самоподписанный, нужно нажать “Advanced → Proceed anyway” в браузере.
