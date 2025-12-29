
## DevOps лабораторная 3

Выполнили: Бен Шамех Абделазиз, Абаккар Иссака Малли

## Цель

Написать "плохой" CI/CD файл с минимум 3 bad practices, разобрать почему они плохие, написать "хороший" CI/CD где все исправлено.
Реализация

Сначала зашли в папку Lab3 и создали простой Node.js проект:

````
npm init -y
````
<img width="536" height="275" alt="lab30" src="https://github.com/user-attachments/assets/183769b7-c991-42bb-bfac-b046fae8d148" />


Добавили в package.json скрипты:

````
"scripts": {
  "test": "echo 'All tests passed' && exit 0",
  "build": "echo 'Build complete'"
}
````
Проверили локально:

````
npm test
npm run build
````
<img width="445" height="261" alt="lab36" src="https://github.com/user-attachments/assets/d043ceb0-c82c-492f-b2eb-feefa2cbf94d" />


Создали папки:

````
mkdir -p .github/workflows
mkdir screenshots
````

<img width="427" height="54" alt="lab31" src="https://github.com/user-attachments/assets/1ffd09b0-5aa0-49db-b981-8fc14ea06162" />

## Плохой CI/CD (bad-ci.yml)

````
name: Bad CI/CD
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - run: git clone https://github.com/AbdelazizBenChamekh/Cloud_Technologies_Part1.git .
    - run: echo "API_KEY=supersecret12345" >> .env
    - run: sudo npm install
    - run: npm test || true
    - run: npm run build
````
<img width="671" height="248" alt="lab33" src="https://github.com/user-attachments/assets/c021125d-ab0c-408e-848b-749f84557f51" />

## Хороший CI/CD (good-ci.yml)

````
name: Good CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
env:
  NODE_VERSION: '20'
jobs:
  test:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    - run: npm ci
    - run: npm test
  build:
    runs-on: ubuntu-22.04
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    - run: npm ci
    - run: npm run build
````
<img width="505" height="551" alt="lab37" src="https://github.com/user-attachments/assets/22a621f7-0ba0-411f-9ba6-5a47bbefe6bb" />


Коммитим:

````
git add .
git status
git commit -m "Lab3: bad + good CI/CD"
git push origin main
````

## Разбор BAD Practices

В плохом файле 6 реальных проблем:

    ubuntu-latest - завтра GitHub обновит раннеры и все сломается
    Фикс: ubuntu-22.04 - конкретная стабильная версия

    git clone вручную - не работает с приватными репами, submodules
    Фикс: actions/checkout@v4 - официальное действие с GITHUB_TOKEN

    echo "API_KEY=..." - секрет виден всем в логах Actions!
    Фикс: ${{ secrets.API_KEY }} из GitHub Secrets

    sudo npm install - проблемы с правами, лишние привилегии
    Фикс: actions/setup-node@v4 - правильно настраивает Node.js

    npm test || true - тесты упали? Не важно, все равно green!
    Фикс: Обычный npm test - падает при ошибках

    Все в одном job - где именно сломалось? Не понятно
    Фикс: Отдельные jobs test → build с needs

<img width="1920" height="563" alt="FINAL" src="https://github.com/user-attachments/assets/b1844cc4-ec0c-4040-8c01-7468183fa76e" />


<img width="1920" height="556" alt="bad" src="https://github.com/user-attachments/assets/cafe98c5-5a4d-4605-bf2a-97cde17d9579" />


<img width="1920" height="556" alt="bad" src="https://github.com/user-attachments/assets/8f2a9bd6-c4ac-49ff-b307-9fc81127130f" />

## Итоги

Оба пайплайна дали зеленые галочки, но разница огромная:

    Плохой: небезопасный, медленный, ненадежный

    Хороший: безопасный, с кэшем (быстрее в 2 раза), падает при ошибках
