---
description: Referencia completa del cliente CNE para consultar el registro electoral venezolano por cédula de identidad.
---

# Cliente CNE

El cliente CNE permite consultar el registro electoral del Consejo Nacional Electoral (CNE) de Venezuela por cédula de identidad. Retorna datos del votante como nombre completo, estado, municipio, parroquia y centro de votación.

## Funciones disponibles

### `query_id`

Consulta los datos electorales de una persona por su cédula de identidad.

```python
from pyvenezuela import query_id
from pyvenezuela import NationalityEnum

persona = query_id(
    nationality=NationalityEnum.VENEZUELAN,
    id="12345678",
)
# -> CNEPersonaModel | None
```

**Parámetros:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `nationality` | `NationalityEnum` | Tipo de cédula (`V` venezolano o `E` extranjero) |
| `id` | `str` | Número de cédula (sin prefijo V- o E-) |

**Retorna:** `CNEPersonaModel` con los datos del votante, o `None` si:

- La cédula no está registrada en el CNE
- El sitio del CNE no está disponible (error HTTP)
- La respuesta no tiene el formato esperado

---

## Modelos

### `CNEPersonaModel`

Datos electorales de una persona registrada en el CNE.

```python
from pyvenezuela import CNEPersonaModel

persona: CNEPersonaModel
persona.id                      # str — cédula con prefijo (ej. "V-12345678")
persona.full_name               # str — nombre completo
persona.state                   # str — estado
persona.municipality            # str — municipio
persona.parish                  # str — parroquia
persona.voting_center           # str — nombre del centro de votación
persona.voting_center_address   # str — dirección del centro de votación
```

---

## Enums

### `NationalityEnum`

| Valor | Código | Descripción |
|-------|--------|-------------|
| `NationalityEnum.VENEZUELAN` | `V` | Cédula venezolana |
| `NationalityEnum.FOREIGNER` | `E` | Cédula de extranjero residente |

---

## Ejemplos

### Consulta básica

```python
from pyvenezuela import query_id, NationalityEnum

persona = query_id(nationality=NationalityEnum.VENEZUELAN, id="12345678")

if persona:
    print(f"Nombre:    {persona.full_name}")
    print(f"Estado:    {persona.state}")
    print(f"Municipio: {persona.municipality}")
    print(f"Parroquia: {persona.parish}")
    print(f"Centro:    {persona.voting_center}")
    print(f"Dirección: {persona.voting_center_address}")
else:
    print("Cédula no encontrada o servicio no disponible.")
```

### Consulta de extranjero

```python
from pyvenezuela import query_id, NationalityEnum

persona = query_id(nationality=NationalityEnum.FOREIGNER, id="87654321")

if persona:
    print(f"{persona.id} — {persona.full_name}")
```

### Manejo robusto de errores

```python
from pyvenezuela import query_id, NationalityEnum, CNEPersonaModel
from typing import Optional

def buscar_cedula(cedula: str) -> Optional[CNEPersonaModel]:
    # Determinar si es venezolano o extranjero por el prefijo
    if cedula.upper().startswith("V-"):
        nationality = NationalityEnum.VENEZUELAN
        numero = cedula[2:]
    elif cedula.upper().startswith("E-"):
        nationality = NationalityEnum.FOREIGNER
        numero = cedula[2:]
    else:
        nationality = NationalityEnum.VENEZUELAN
        numero = cedula

    return query_id(nationality=nationality, id=numero)


persona = buscar_cedula("V-12345678")
if persona:
    print(persona.model_dump())
```

!!! tip
    El CNE puede responder lentamente o no estar disponible en ciertos momentos.
    Considera implementar reintentos con backoff exponencial para aplicaciones en producción.
