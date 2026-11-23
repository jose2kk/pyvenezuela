"""CNE Client."""

import re

import requests

from pyvenezuela.schemas import cne as cne_schemas
from pyvenezuela.schemas import persona as persona_schemas

BASE_URL = "http://www.cne.gob.ve/web/registro_electoral/ce.php"
PATTERNS = dict(
    id=r'Cédula:</font></b></td>\s*<td align="left">(.*?)</td>',
    full_name=r'Nombre:</font></b></td>\s*<td align="left"><b>(.*?)</b></td>',
    state=r'Estado:</font></b></td>\s*<td align="left">(.*?)</td>',
    municipality=r'Municipio:</font></b></td.*?>\s*<td align="left">(.*?)</td>',
    parish=r'Parroquia:</font.*?></b></td>\s*<td align="left">(.*?)</td>',
    voting_center=(
        r'Centro:</font></b></td>\s*<td align="left">'
        r'<font color="#0000FF">(.*?)</font></td>'
    ),
    voting_center_address=(
        r'Dirección:</font></b></td>\s*<td align="left">'
        r'<font color="#0000FF">(.*?)</font></td>'
    ),
)


def query_id(
    nationality: cne_schemas.NationalityEnum, id: persona_schemas.ID
) -> cne_schemas.CNEPersonaModel | None:
    try:
        response = requests.get(url=BASE_URL, params=dict(nacionalidad=nationality, cedula=id))
        response.raise_for_status()
    except requests.HTTPError:
        return None

    data = {}
    for key, pattern in PATTERNS.items():
        match = re.search(pattern, response.text, re.DOTALL)
        if match is None:
            return None
        data[key] = match.group(1).strip()
    return cne_schemas.CNEPersonaModel.model_validate(data)
