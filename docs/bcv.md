---
description: Referencia completa del cliente BCV para obtener tasas de cambio del Banco Central de Venezuela.
---

# Cliente BCV

El cliente BCV permite obtener las tasas de cambio publicadas por el Banco Central de Venezuela (BCV), tanto las tasas oficiales publicadas en el sitio web del BCV como las tasas reportadas por cada banco del sistema financiero venezolano.

## Funciones disponibles

### `get_rates_by_bcv`

Retorna las tasas de cambio publicadas directamente en el sitio web del BCV.

```python
from pyvenezuela import get_rates_by_bcv
from pyvenezuela import BCVCurrencyEnum

rates = get_rates_by_bcv()
# -> dict[BCVCurrencyEnum, float] | None
```

**Retorna:** `dict[BCVCurrencyEnum, float]` con las tasas en bolívares por unidad de moneda extranjera, o `None` si el sitio no está disponible.

**Caché:** Los resultados se cachean por 8 horas en memoria. Si ocurre un error al actualizar, se retorna el último valor válido.

```python
if rates:
    usd = rates[BCVCurrencyEnum.USD]
    eur = rates[BCVCurrencyEnum.EUR]
    print(f"1 USD = {usd:.4f} Bs.")
    print(f"1 EUR = {eur:.4f} Bs.")
```

---

### `get_rates`

Retorna las tasas de todos los bancos del sistema para un rango de fechas.

```python
from pyvenezuela import get_rates
import datetime

# Últimos 30 días (por defecto)
rates = get_rates()

# Rango específico
rates = get_rates(
    start_date=datetime.date(2024, 1, 1),
    end_date=datetime.date(2024, 1, 31),
)
# -> dict[BankEnum, list[BCVBankRatesModel]] | None
```

**Parámetros:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `start_date` | `datetime.date \| None` | Inicio del rango (por defecto: hace 30 días) |
| `end_date` | `datetime.date \| None` | Fin del rango (por defecto: hoy) |

**Retorna:** Diccionario con cada banco y su lista de tasas históricas, o `None` si el sitio no está disponible.

---

### `get_rates_by_bank`

Retorna las tasas de un banco específico para un rango de fechas.

```python
from pyvenezuela import get_rates_by_bank
from pyvenezuela import BankEnum
import datetime

rates = get_rates_by_bank(
    bank=BankEnum.BANCO_DE_VENEZUELA,
    start_date=datetime.date(2024, 1, 1),
    end_date=datetime.date(2024, 1, 31),
)
# -> list[BCVBankRatesModel]
```

**Parámetros:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `bank` | `BankEnum` | Banco a consultar |
| `start_date` | `datetime.date \| None` | Inicio del rango |
| `end_date` | `datetime.date \| None` | Fin del rango |

**Retorna:** Lista de `BCVBankRatesModel`. Retorna lista vacía si no hay datos disponibles.

---

## Modelos

### `BCVBankRatesModel`

Tasa de cambio de un banco para una fecha específica.

```python
from pyvenezuela import BCVBankRatesModel

rate: BCVBankRatesModel
rate.date        # datetime.date — fecha de la tasa
rate.buy_rate    # float — tasa de compra (Bs. por USD)
rate.sell_rate   # float — tasa de venta (Bs. por USD)
```

---

## Enums

### `BCVCurrencyEnum`

Monedas publicadas en el sitio del BCV.

| Valor | Descripción |
|-------|-------------|
| `BCVCurrencyEnum.USD` | Dólar estadounidense |
| `BCVCurrencyEnum.EUR` | Euro |
| `BCVCurrencyEnum.CNY` | Yuan chino |
| `BCVCurrencyEnum.TRY` | Lira turca |
| `BCVCurrencyEnum.RUB` | Rublo ruso |

### `BankEnum`

Bancos del sistema financiero venezolano disponibles.

```python
from pyvenezuela import BankEnum

BankEnum.BANCAMIGA
BankEnum.BANCARIBE
BankEnum.BANCO_ACTIVO
BankEnum.BANCO_BICENTENARIO_DEL_PUEBLO
BankEnum.BANCO_DE_VENEZUELA
BankEnum.BANCO_DELSUR
BankEnum.BANCO_DEL_TESORO
BankEnum.BANCO_EXTERIOR
BankEnum.BANCO_FONDO_COMUN
BankEnum.BANCO_NACIONAL_DE_CREDITO
BankEnum.BANCO_OCCIDENTAL_DE_DESCUENTO
BankEnum.BANCO_PLAZA
BankEnum.BANCO_SOFITASA
BankEnum.BANCO_VENEZOLANO_DE_CREDITO
BankEnum.BANESCO
BankEnum.BANPLUS
BankEnum.BANCO_MERCANTIL
BankEnum.BBVA_PROVINCIAL
BankEnum.CIEN_PC_BANCO
BankEnum.CITIBANK
BankEnum.MI_BANCO
BankEnum.OTHER_BANKS
```

---

## Ejemplo completo

```python
from pyvenezuela import get_rates_by_bcv, get_rates_by_bank
from pyvenezuela import BCVCurrencyEnum, BankEnum
import datetime

# Tasa oficial BCV
rates = get_rates_by_bcv()
if rates:
    print(f"Tasa BCV hoy: 1 USD = {rates[BCVCurrencyEnum.USD]:.4f} Bs.")

# Historial de un banco (último mes)
hoy = datetime.date.today()
hace_un_mes = hoy - datetime.timedelta(days=30)

banesco_rates = get_rates_by_bank(
    bank=BankEnum.BANESCO,
    start_date=hace_un_mes,
    end_date=hoy,
)

print(f"\nTasas Banesco (últimos 30 días): {len(banesco_rates)} registros")
for rate in banesco_rates[-5:]:  # últimos 5
    print(f"  {rate.date}  compra: {rate.buy_rate:.4f}  venta: {rate.sell_rate:.4f}")
```
