---
description: Cómo instalar pyvenezuela y realizar las primeras consultas al BCV y CNE.
---

# Guía de inicio

## Instalación

### pip

```sh
pip install pyvenezuela
```

### uv

```sh
uv add pyvenezuela
```

### Desde el código fuente

```sh
git clone https://github.com/jose2kk/pyvenezuela.git
cd pyvenezuela
uv sync
```

## Requisitos

- Python 3.10 o superior
- Conexión a internet (para consultas al BCV y CNE)

## Tu primera consulta al BCV

Obtén las tasas de cambio publicadas por el Banco Central de Venezuela:

```python
from pyvenezuela import get_rates_by_bcv
from pyvenezuela import BCVCurrencyEnum

rates = get_rates_by_bcv()

if rates:
    print(f"Dólar (USD): {rates[BCVCurrencyEnum.USD]:.4f} Bs.")
    print(f"Euro (EUR):  {rates[BCVCurrencyEnum.EUR]:.4f} Bs.")
    print(f"Yuan (CNY):  {rates[BCVCurrencyEnum.CNY]:.4f} Bs.")
```

!!! note
    `get_rates_by_bcv()` retorna `None` si el sitio del BCV no está disponible.
    Los resultados se cachean automáticamente por 8 horas.

## Tu primera consulta al CNE

Busca datos electorales de un ciudadano por su cédula de identidad:

```python
from pyvenezuela import query_id
from pyvenezuela import NationalityEnum

# Venezolano
persona = query_id(nationality=NationalityEnum.VENEZUELAN, id="12345678")

# Extranjero
persona_ext = query_id(nationality=NationalityEnum.FOREIGNER, id="87654321")

if persona:
    print(f"Nombre:        {persona.full_name}")
    print(f"Estado:        {persona.state}")
    print(f"Municipio:     {persona.municipality}")
    print(f"Parroquia:     {persona.parish}")
    print(f"Centro:        {persona.voting_center}")
    print(f"Dirección:     {persona.voting_center_address}")
```

!!! warning
    `query_id()` retorna `None` si la cédula no se encuentra en el registro
    o si el sitio del CNE no está disponible.

## Tasas por banco

Consulta las tasas de compra y venta reportadas por un banco específico:

```python
from pyvenezuela import get_rates_by_bank
from pyvenezuela import BankEnum

rates = get_rates_by_bank(bank=BankEnum.BANESCO)

for rate in rates:
    print(f"{rate.date}  compra: {rate.buy_rate:.4f}  venta: {rate.sell_rate:.4f}")
```

## Todos los bancos a la vez

```python
from pyvenezuela import get_rates
from pyvenezuela import BankEnum

all_rates = get_rates()

if all_rates:
    for bank, rates in all_rates.items():
        if rates:
            latest = rates[-1]
            print(f"{bank.value}: {latest.sell_rate:.4f}")
```

## Próximos pasos

- [Cliente BCV](bcv.md) — referencia completa incluyendo filtros por fecha y enums disponibles
- [Cliente CNE](cne.md) — detalles del modelo de respuesta y manejo de errores
- [Sistema de caché](cache.md) — cómo personalizar el caché o deshabilitarlo
