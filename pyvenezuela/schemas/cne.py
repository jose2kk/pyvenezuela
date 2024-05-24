"""CNE Schemas."""

import enum

from pydantic import BaseModel

from pyvenezuela.schemas import persona as persona_schemas


class NationalityEnum(str, enum.Enum):
    """Nationality Enum."""

    VENEZUELAN = "V"
    FOREIGNER = "E"


class CNEPersonaModel(BaseModel):
    """CNE Persona Model."""

    id: persona_schemas.ID  # cedula
    full_name: str  # nombre completo
    state: str  # estado
    municipality: str  # municipio
    parish: str  # parroquia
    voting_center: str  # centro de votacion
    voting_center_address: str  # direccion del centro de votacion
