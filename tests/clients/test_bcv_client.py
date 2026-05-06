"""BCV Client Tests."""

import datetime

import requests
import requests_mock

from pyvenezuela.cache import inmemory_cache
from pyvenezuela.clients import bcv as bcv_client
from pyvenezuela.schemas import bcv as bcv_schemas


def _clear_bcv_cache() -> None:
    """Clear the inmemory_cache to avoid test pollution from the @cached decorator."""
    inmemory_cache.cache.clear()


BCV_HOMEPAGE_HTML = """
<html>
<body>
<div id="euro"><strong>  40,12345678  </strong></div>
<div id="yuan"><strong>  5,67891234  </strong></div>
<div id="lira"><strong>  1,23456789  </strong></div>
<div id="rublo"><strong>  0,45678912  </strong></div>
<div id="dolar"><strong>  36,71520000  </strong></div>
</body>
</html>
"""

BCV_HOMEPAGE_MISSING_ELEMENTS_HTML = """
<html>
<body>
<div id="euro"><strong>  40,12345678  </strong></div>
<div id="yuan"><strong>  5,67891234  </strong></div>
</body>
</html>
"""

BANK_RATES_HTML = """
<html>
<body>
<table>
<tr>
<td>01-04-2026</td>
<td>Banesco</td>
<td>36,5000</td>
<td>36,7000</td>
</tr>
<tr>
<td>01-04-2026</td>
<td>Banco de Venezuela</td>
<td>36,4500</td>
<td>36,6500</td>
</tr>
<tr>
<td>15-03-2026</td>
<td>Banesco</td>
<td>35,5000</td>
<td>35,7000</td>
</tr>
</table>
</body>
</html>
"""


def test_get_rates_by_bcv__successful(requests_mock: requests_mock.Mocker) -> None:
    _clear_bcv_cache()
    requests_mock.get(url=bcv_client.BCV_URL, text=BCV_HOMEPAGE_HTML)

    result = bcv_client.get_rates_by_bcv()

    assert result is not None
    assert result[bcv_schemas.BCVCurrencyEnum.EUR] == 40.12345678
    assert result[bcv_schemas.BCVCurrencyEnum.CNY] == 5.67891234
    assert result[bcv_schemas.BCVCurrencyEnum.TRY] == 1.23456789
    assert result[bcv_schemas.BCVCurrencyEnum.RUB] == 0.45678912
    assert result[bcv_schemas.BCVCurrencyEnum.USD] == 36.71520000


def test_get_rates_by_bcv__missing_elements_returns_none(
    requests_mock: requests_mock.Mocker,
) -> None:
    _clear_bcv_cache()
    requests_mock.get(url=bcv_client.BCV_URL, text=BCV_HOMEPAGE_MISSING_ELEMENTS_HTML)

    result = bcv_client.get_rates_by_bcv()

    assert result is None


def test_get_rates_by_bcv__http_error_returns_none(
    requests_mock: requests_mock.Mocker,
) -> None:
    _clear_bcv_cache()
    requests_mock.get(url=bcv_client.BCV_URL, exc=requests.HTTPError)

    result = bcv_client.get_rates_by_bcv()

    assert result is None


def test_get_rates__successful(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(url=bcv_client.RATES_URL, text=BANK_RATES_HTML)

    result = bcv_client.get_rates(
        start_date=datetime.date(2026, 3, 1),
        end_date=datetime.date(2026, 4, 30),
    )

    assert result is not None
    assert bcv_schemas.BankEnum.BANESCO in result
    assert bcv_schemas.BankEnum.BANCO_DE_VENEZUELA in result

    banesco_rates = result[bcv_schemas.BankEnum.BANESCO]
    assert len(banesco_rates) == 2
    assert banesco_rates[0].buy_rate == 36.5
    assert banesco_rates[0].sell_rate == 36.7
    assert banesco_rates[0].date == datetime.date(2026, 4, 1)


def test_get_rates__start_date_after_end_date_returns_none(
    requests_mock: requests_mock.Mocker,
) -> None:
    result = bcv_client.get_rates(
        start_date=datetime.date(2026, 5, 1),
        end_date=datetime.date(2026, 4, 1),
    )

    assert result is None


def test_get_rates__http_error_returns_none(
    requests_mock: requests_mock.Mocker,
) -> None:
    requests_mock.get(url=bcv_client.RATES_URL, exc=requests.HTTPError)

    result = bcv_client.get_rates(
        start_date=datetime.date(2026, 3, 1),
        end_date=datetime.date(2026, 4, 30),
    )

    assert result is None


def test_get_rates_by_bank__successful(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(url=bcv_client.RATES_URL, text=BANK_RATES_HTML)

    result = bcv_client.get_rates_by_bank(
        bank=bcv_schemas.BankEnum.BANESCO,
        start_date=datetime.date(2026, 3, 1),
        end_date=datetime.date(2026, 4, 30),
    )

    assert len(result) == 2
    assert result[0].date == datetime.date(2026, 4, 1)
    assert result[0].buy_rate == 36.5


def test_get_rates_by_bank__bank_not_in_results_returns_empty(
    requests_mock: requests_mock.Mocker,
) -> None:
    requests_mock.get(url=bcv_client.RATES_URL, text=BANK_RATES_HTML)

    result = bcv_client.get_rates_by_bank(
        bank=bcv_schemas.BankEnum.BANCARIBE,
        start_date=datetime.date(2026, 3, 1),
        end_date=datetime.date(2026, 4, 30),
    )

    assert result == []


def test_get_rates__date_filtering(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(url=bcv_client.RATES_URL, text=BANK_RATES_HTML)

    result = bcv_client.get_rates(
        start_date=datetime.date(2026, 4, 1),
        end_date=datetime.date(2026, 4, 30),
    )

    assert result is not None
    # Only April data should be included, not the March 15 entry
    banesco_rates = result.get(bcv_schemas.BankEnum.BANESCO, [])
    assert len(banesco_rates) == 1
    assert banesco_rates[0].date == datetime.date(2026, 4, 1)
