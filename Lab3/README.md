
## DevOps лабораторная 3

Выполнили: Бен Шамех Абделазиз, Абаккар Иссака Малли

## Цель

Написать "плохой" CI/CD файл с минимум 3 bad practices, разобрать почему они плохие, написать "хороший" CI/CD где все исправлено.
Реализация

Сначала зашли в папку Lab3 и создали простой Node.js проект:

````
npm init -y
````

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
📸 Скриншот 1: npm test и build работают локально

Создали папки:

````
mkdir -p .github/workflows
mkdir screenshots
````

📸 Скриншот 2: Создание папки workflows
Плохой CI/CD (bad-ci.yml)

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
📸 Скриншот 3: Содержимое bad-ci.yml
Хороший CI/CD (good-ci.yml)

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
📸 Скриншот 4: Содержимое good-ci.yml

Коммитим:

````
git add .
git status
git commit -m "Lab3: bad + good CI/CD"
git push origin main
````
📸 Скриншот 5: git status перед пушем

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

📸 Скриншот 6: GitHub Actions - оба workflow зеленые

📸 Скриншот 7: Bad CI/CD детали (ошибки есть, но || true их скрывает)

📸 Скриншот 8: Good CI/CD детали (все чисто и правильно)
## Итоги

Оба пайплайна дали зеленые галочки, но разница огромная:

    Плохой: небезопасный, медленный, ненадежный

    Хороший: безопасный, с кэшем (быстрее в 2 раза), падает при ошибках
