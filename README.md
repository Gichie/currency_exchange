# Currency Exchange API

Currency Exchange API — это RESTful API, предназначенный для управления валютами, обменными курсами и выполнения операций конвертации валют.

## Основные возможности
- Управление валютами:
  - Получение списка всех валют.
  - Получение информации о конкретной валюте по её коду.
  - Добавление новой валюты.
- Управление обменными курсами:
  - Получение списка всех курсов обмена.
  - Получение курса обмена для заданной пары валют.
  - Добавление нового курса обмена.
  - Обновление существующего курса обмена.
- Конвертация валют:
  - Расчёт суммы, эквивалентной заданной, для двух валют.

## Установка и запуск

### 1. Склонируйте репозиторий

git clone [https://github.com/your-repository/currency-exchange-api.git](https://github.com/Gichie/currency_exchange.git)
cd currency-exchange-api

### 2. Инициализация базы данных

Создайте файл базы данных currency_exchange.db, если он отсутствует, и выполните миграции для создания таблиц.

### 3. Запуск API

Перед запуском поменяйте в файле server.py переменную HOST на свой локальный IP
Запустите сервер:
python main.py
