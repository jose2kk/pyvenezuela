---
description: Cómo funciona el sistema de caché de pyvenezuela y cómo implementar tu propio backend.
---

# Sistema de caché

pyvenezuela incluye un sistema de caché que evita peticiones repetidas a los servicios externos. Por defecto usa un caché en memoria (`InMemoryCache`), pero puedes implementar tu propio backend.

## Caché por defecto

La función `get_rates_by_bcv()` usa automáticamente un caché en memoria compartido con un TTL de 8 horas:

```python
from pyvenezuela import get_rates_by_bcv

# Primera llamada: hace la petición al BCV
rates = get_rates_by_bcv()

# Segunda llamada: retorna el valor cacheado (sin petición HTTP)
rates = get_rates_by_bcv()
```

Si el sitio del BCV no está disponible al intentar actualizar la caché, se retorna el último valor válido almacenado (comportamiento `use_expired=True`).

---

## Implementar un caché personalizado

Para usar un backend diferente (Redis, Memcached, base de datos, etc.), extiende la clase abstracta `Cache`:

```python
from typing import Any, Optional
from pyvenezuela.cache import Cache
from pyvenezuela.schemas.cache import CacheValueModel
import time


class RedisCache(Cache):
    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, key: str) -> Optional[CacheValueModel]:
        data = self.redis.get(key)
        if data is None:
            return None
        return CacheValueModel.model_validate_json(data)

    def set(self, key: str, value: Any, ttl_in_seconds: int) -> None:
        model = CacheValueModel(
            value=value,
            expires_at=time.time() + ttl_in_seconds,
        )
        self.redis.setex(key, ttl_in_seconds, model.model_dump_json())
```

---

## Usar el caché personalizado con el decorador

El decorador `cached` puede usarse con cualquier implementación de `Cache`:

```python
from pyvenezuela.cache import Cache
from pyvenezuela.decorators import cached
from pyvenezuela.clients import bcv

redis_cache = RedisCache(redis_client=my_redis)


@cached(
    cache=redis_cache,
    cached_key="bcv_rates",
    ttl_in_seconds=8 * 60 * 60,  # 8 horas
    use_expired=True,
)
def get_rates_con_redis():
    return bcv.get_rates_by_bcv.__wrapped__()
```

---

## API de caché

### `Cache` (clase abstracta)

```python
from pyvenezuela.cache import Cache
from pyvenezuela.schemas.cache import CacheValueModel

class Cache:
    def get(self, key: str) -> Optional[CacheValueModel]: ...
    def set(self, key: str, value: Any, ttl_in_seconds: int) -> None: ...
```

### `InMemoryCache`

Implementación en memoria incluida en la librería.

```python
from pyvenezuela.cache import InMemoryCache

cache = InMemoryCache()
cache.set("mi_clave", {"dato": 42}, ttl_in_seconds=300)
valor = cache.get("mi_clave")
```

### `CacheValueModel`

Modelo interno que almacena el valor y su tiempo de expiración.

```python
from pyvenezuela.schemas.cache import CacheValueModel

model: CacheValueModel
model.value       # Any — el valor almacenado
model.expires_at  # float — timestamp Unix de expiración
```

---

## Decorador `cached`

```python
from pyvenezuela.decorators import cached
from pyvenezuela.cache import InMemoryCache

cache = InMemoryCache()


@cached(
    cache=cache,
    cached_key="clave_unica",
    ttl_in_seconds=3600,
    use_expired=False,  # Si True, retorna el valor expirado cuando falla la actualización
)
def mi_funcion():
    return datos_costosos()
```

**Parámetros del decorador:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `cache` | `Cache` | Instancia del backend de caché |
| `cached_key` | `str` | Clave única para este valor en el caché |
| `ttl_in_seconds` | `int` | Tiempo de vida del caché en segundos |
| `use_expired` | `bool` | Si `True`, retorna el último valor aunque haya expirado cuando la función falla |

!!! tip
    Usa `use_expired=True` para funciones que consultan servicios externos poco confiables.
    Así el sistema degrada graciosamente en lugar de retornar `None`.
