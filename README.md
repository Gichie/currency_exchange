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

git clone https://github.com/your-repository/currency-exchange-api.git
cd currency-exchange-api

### 2. Инициализация базы данных

Создайте файл базы данных currency_exchange.db, если он отсутствует, и выполните миграции для создания таблиц.

### 3. Запуск API

Перед запуском поменяйте в файле server.py переменную HOST на свой локальный IP
Запустите сервер:
python main.py

### Примеры API запросов
## Валюты
# Получение списка всех валют

GET /currencies
Пример ответа:

```json
[
    {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    {
        "id": 0,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
]
```

# Добавление новой валюты

POST /currencies
Пример тела запроса:

{
    "name": "Pound Sterling",
    "code": "GBP",
    "sign": "£"
}

Пример ответа:

{
    "message": "Currency added successfully"
}

## Обменные курсы
# Получение курса обмена для пары валют

GET /exchangeRate/USD-EUR
Пример ответа:

{
    "id": 1,
    "base_currency": {
        "id": 1,
        "code": "USD",
        "name": "US Dollar",
        "sign": "$"
    },
    "target_currency": {
        "id": 2,
        "code": "EUR",
        "name": "Euro",
        "sign": "€"
    },
    "rate": 1.1
}

# Добавление нового курса обмена

POST /exchangeRates
Пример тела запроса:

{
    "baseCurrencyCode": "USD",
    "targetCurrencyCode": "JPY",
    "rate": 110.5
}

Пример ответа:

{
    "message": "Exchange rate added successfully"
}

# Конвертация валют

GET /exchange?from_currency=USD&to_currency=EUR&amount=100
Пример ответа:

{
    "baseCurrency": "USD",
    "targetCurrency": "EUR",
    "rate": 1.1,
    "amount": 100.0,
    "convertedAmount": 110.0
}
