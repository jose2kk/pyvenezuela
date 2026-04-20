<p align="center">
  <img src="https://raw.githubusercontent.com/jose2kk/pyvenezuela/main/public/logo.png" alt="pyvenezuela">
</p>
<p align="center">
    <em>Python library to query Venezuela's data</em>
</p>
<p align="center">
<a href="https://github.com/jose2kk/pyvenezuela/actions?query=workflow:CI+branch:main" target="_blank">
    <img src="https://github.com/jose2kk/pyvenezuela/workflows/CI/badge.svg" alt="CI">
</a>
<a href="https://pypi.org/project/pyvenezuela" target="_blank">
    <img src="https://img.shields.io/pypi/v/pyvenezuela?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pyvenezuela" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pyvenezuela.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Docs**: <a href="https://pyvenezuela.jose2kk.com" target="_blank">https://pyvenezuela.jose2kk.com</a>

**Source Code**: <a href="https://github.com/jose2kk/pyvenezuela" target="_blank">https://github.com/jose2kk/pyvenezuela</a>

---

pyvenezuela is a Python library for querying Venezuelan public data sources, including exchange rates from the Central Bank of Venezuela (BCV) and voter data from the National Electoral Council (CNE).

## Features

- **BCV exchange rates** — official rates (USD, EUR, CNY, TRY, RUB) from the BCV website
- **Bank rates** — buy/sell rates reported by all Venezuelan banks
- **CNE voter lookup** — query voter registration data by ID number
- **In-memory cache** — automatic TTL-based caching to reduce HTTP requests
- **Custom cache backends** — plug in Redis, Memcached, or any other store
- **Typed responses** — Pydantic v2 models with full type annotations

## Installation

```sh
pip install pyvenezuela
```

Or with [uv](https://docs.astral.sh/uv/):

```sh
uv add pyvenezuela
```

## Quick Start

### BCV Exchange Rates

```python
from pyvenezuela import get_rates_by_bcv, BCVCurrencyEnum

rates = get_rates_by_bcv()
if rates:
    print(f"USD: {rates[BCVCurrencyEnum.USD]:.4f} Bs.")
    print(f"EUR: {rates[BCVCurrencyEnum.EUR]:.4f} Bs.")
```

### Bank Rates

```python
from pyvenezuela import get_rates_by_bank, BankEnum
import datetime

today = datetime.date.today()
last_month = today - datetime.timedelta(days=30)

rates = get_rates_by_bank(
    bank=BankEnum.BANESCO,
    start_date=last_month,
    end_date=today,
)

for rate in rates:
    print(f"{rate.date}  buy: {rate.buy_rate:.4f}  sell: {rate.sell_rate:.4f}")
```

### CNE Voter Lookup

```python
from pyvenezuela import query_id, NationalityEnum

persona = query_id(nationality=NationalityEnum.VENEZUELAN, id="12345678")
if persona:
    print(f"Name:          {persona.full_name}")
    print(f"State:         {persona.state}")
    print(f"Voting center: {persona.voting_center}")
```

## Development

```sh
# Install dependencies
uv sync --locked

# Run tests
make test

# Lint + type check
make check

# Format code
make format
```

## Requirements

- Python 3.10+
- Dependencies: `beautifulsoup4`, `pydantic>=2`, `requests`

## License

MIT
