"""CNE Client Tests."""

import requests
import requests_mock

from pyvenezuela.clients import cne as cne_client
from pyvenezuela.schemas import cne as cne_schemas
from tests.conftest import (
    build_query_id_response_incomplete_text,
    build_query_id_response_text,
)


def test_query_id__successfull(
    cne_persona_model: cne_schemas.CNEPersonaModel, requests_mock: requests_mock.Mocker
) -> None:
    nationality, id = cne_persona_model.id.split("-")
    requests_mock.get(
        url=f"{cne_client.BASE_URL}?nacionalidad={nationality}&cedula={id}",
        text=build_query_id_response_text(cne_persona=cne_persona_model),
    )
    assert cne_client.query_id(nationality=nationality, id=id) == cne_persona_model


def test_query_id__validation_error(
    cne_persona_model: cne_schemas.CNEPersonaModel, requests_mock: requests_mock.Mocker
) -> None:
    nationality, id = cne_persona_model.id.split("-")
    requests_mock.get(
        url=f"{cne_client.BASE_URL}?nacionalidad={nationality}&cedula={id}",
        text=build_query_id_response_incomplete_text(),
    )
    assert cne_client.query_id(nationality=nationality, id=id) is None


def test_query_id__http_error(
    cne_persona_model: cne_schemas.CNEPersonaModel, requests_mock: requests_mock.Mocker
) -> None:
    nationality, id = cne_persona_model.id.split("-")
    requests_mock.get(
        url=f"{cne_client.BASE_URL}?nacionalidad={nationality}&cedula={id}",
        exc=requests.HTTPError,
    )
    assert cne_client.query_id(nationality=nationality, id=id) is None
