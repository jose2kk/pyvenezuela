"""CNE Client."""

import re
from typing import Optional

import requests
from pyvenezuela.schemas import (
    cne as cne_schemas,
    persona as persona_schemas,
)

BASE_URL = "http://www.cne.gob.ve/web/registro_electoral/ce.php"
PATTERNS = dict(
    id=r'Cédula:</font></b></td>\s*<td align="left">(.*?)</td>',
    full_name=r'Nombre:</font></b></td>\s*<td align="left"><b>(.*?)</b></td>',
    state=r'Estado:</font></b></td>\s*<td align="left">(.*?)</td>',
    municipality=r'Municipio:</font></b></td.*?>\s*<td align="left">(.*?)</td>',
    parish=r'Parroquia:</font.*?></b></td>\s*<td align="left">(.*?)</td>',
    voting_center=r'Centro:</font></b></td>\s*<td align="left"><font color="#0000FF">(.*?)</font></td>',
    voting_center_address=r'Dirección:</font></b></td>\s*<td align="left"><font color="#0000FF">(.*?)</font></td>',
)


def query_id(
    nationality: cne_schemas.NationalityEnum,
    id: persona_schemas.ID,
) -> Optional[cne_schemas.CNEPersonaModel]:
    try:
        response = requests.get(
            url=BASE_URL,
            params=dict(
                nacionalidad=nationality,
                cedula=id,
            ),
        )
        response.raise_for_status()
        return cne_schemas.CNEPersonaModel.model_validate({
            key: re.search(pattern, response.text, re.DOTALL).group(1).strip()
            for key, pattern in PATTERNS.items()
        })
    except requests.HTTPError:
        return None
    except AttributeError:
        return None


if __name__ == "__main__":
    query_id(nationality=cne_schemas.NationalityEnum.VENEZUELAN, number="20726224")
