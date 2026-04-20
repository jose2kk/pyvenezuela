---
description: pyvenezuela es una librería Python para consultar datos de Venezuela, incluyendo tasas de cambio del BCV y datos del registro electoral del CNE.
---

# pyvenezuela

**Consulta datos de Venezuela con Python.**

pyvenezuela te permite obtener tasas de cambio publicadas por el BCV (Banco Central de Venezuela) y consultar datos del registro electoral del CNE (Consejo Nacional Electoral) directamente desde tu código Python.

## Características

- **Tasas BCV** — obtén el dólar, euro, yuan, lira y rublo publicados por el BCV
- **Tasas por banco** — consulta las tasas de compra/venta reportadas por cada banco venezolano
- **Registro electoral CNE** — busca datos electorales por cédula de identidad (venezolanos y extranjeros)
- **Caché en memoria** — resultados cacheados con TTL para reducir peticiones repetidas
- **Caché personalizable** — implementa tu propio backend de caché (Redis, Memcached, etc.)
- **Modelos Pydantic** — respuestas tipadas y validadas

## Ejemplo rápido

```python
from pyvenezuela import get_rates_by_bcv, query_id
from pyvenezuela import BCVCurrencyEnum, NationalityEnum

# Tasas publicadas por el BCV
rates = get_rates_by_bcv()
if rates:
    print(f"USD/VES: {rates[BCVCurrencyEnum.USD]:.4f}")
    print(f"EUR/VES: {rates[BCVCurrencyEnum.EUR]:.4f}")

# Consulta en el CNE
persona = query_id(nationality=NationalityEnum.VENEZUELAN, id="12345678")
if persona:
    print(f"Nombre: {persona.full_name}")
    print(f"Centro de votación: {persona.voting_center}")
```

## Instalación

=== "pip"

    ```sh
    pip install pyvenezuela
    ```

=== "uv"

    ```sh
    uv add pyvenezuela
    ```

## Próximos pasos

- [Guía de inicio](inicio.md) — instala pyvenezuela y realiza tus primeras consultas
- [Cliente BCV](bcv.md) — referencia completa para tasas de cambio
- [Cliente CNE](cne.md) — referencia para el registro electoral
- [Sistema de caché](cache.md) — configura el caché para tus necesidades
