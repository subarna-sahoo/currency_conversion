# Currency Conversion (Forex App prototype)

A Django prototype for comparing currency pairs:

- **Historical chart** of the exchange rate between any two currencies
- **Forecast** of upcoming business days' rates using a **moving average**

It was hosted on AWS at the time.

## Tech stack

Python · Django 2.2 · Django REST Framework · requests-cache · Chart.js · SQLite

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver          # http://localhost:8000
```

## Routes

| Path | Description |
|---|---|
| `/` | Home |
| `/login/` | Log in |
| `/currency/` | Currency pair list and chart |
| `/currency/get_rates` | JSON endpoint (POST) returning historical and forecast rates for the chart |

## Data source

Rates come from [`exchangeratesapi.io`](https://exchangeratesapi.io), with responses cached by `requests-cache`.

> **Note:** exchangeratesapi.io now requires an API key, and the `/history` endpoint used here has been replaced. To run this today, switch to the provider's current timeseries endpoint (with an access key) or to a free alternative such as [Frankfurter](https://www.frankfurter.app).
