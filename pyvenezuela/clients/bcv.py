"""BCV Client."""

import collections
import datetime
import re

import bs4
import requests

from pyvenezuela.cache import inmemory_cache
from pyvenezuela.decorators import cached
from pyvenezuela.schemas import bcv as bcv_schemas

BCV_URL = "https://www.bcv.org.ve/"
RATES_URL = "https://www.bcv.org.ve/cambiaria/export/tasas-informativas-sistema-bancario"


def _request(url: str) -> bs4.BeautifulSoup | None:
    try:
        response = requests.get(
            url=url,
            verify=False,  # TODO: figure out what to do here with an actual certificate
        )
        response.raise_for_status()
        return bs4.BeautifulSoup(response.content, "html.parser")
    except requests.HTTPError:
        return None


def _get_bcv_soup() -> bs4.BeautifulSoup | None:
    return _request(url=BCV_URL)


def _get_banks_soup() -> bs4.BeautifulSoup | None:
    return _request(url=RATES_URL)


def _get_rates(
    start_date: datetime.date | None = None, end_date: datetime.date | None = None
) -> dict[bcv_schemas.BankEnum, list[bcv_schemas.BCVBankRatesModel]] | None:
    if start_date and end_date and start_date > end_date:
        return None

    if not (start_date and end_date):
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=30)

    soup = _get_banks_soup()
    if not soup:
        return None

    data: dict[str, list[dict[str, str]]] = collections.defaultdict(list)

    rows: list[bs4.element.Tag] = soup.find_all(name="tr")
    for row in rows:
        columns: list[bs4.element.Tag] = row.find_all(name="td")
        if not columns or len(columns) < 4:
            # skipping unsupported format
            continue

        bank = columns[1].text.strip()
        date = columns[0].text.strip()
        buy_rate = columns[2].text.strip().replace(",", ".")
        sell_rate = columns[3].text.strip().replace(",", ".")

        if not (bank and date and buy_rate and sell_rate):
            # skipping incomplete data
            continue

        if not (
            datetime.datetime.strptime(date, "%d-%m-%Y").date() >= start_date
            and datetime.datetime.strptime(date, "%d-%m-%Y").date() <= end_date
        ):
            # skipping out of range data
            continue

        data[bank].append(dict(date=date, buy_rate=buy_rate, sell_rate=sell_rate))

    return bcv_schemas.BCVBanksRatesModel.model_validate(data).root


def _parse_bcv_rate(text: str) -> float:
    return float(re.sub(pattern=r"[^\d,]", repl="", string=text).replace(",", "."))


def get_rates(
    start_date: datetime.date | None = None, end_date: datetime.date | None = None
) -> dict[bcv_schemas.BankEnum, list[bcv_schemas.BCVBankRatesModel]] | None:
    return _get_rates(start_date=start_date, end_date=end_date)


def get_rates_by_bank(
    bank: bcv_schemas.BankEnum,
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
) -> list[bcv_schemas.BCVBankRatesModel]:
    rates = _get_rates(start_date=start_date, end_date=end_date)

    return rates.get(bank, []) if rates else []


# TODO: This decorator should take bcv chanmges into account
@cached(
    cache=inmemory_cache,
    cached_key="bcv_rates_by_bcv",
    ttl_in_seconds=8 * 60 * 60,
    use_expired=True,
)
def get_rates_by_bcv() -> dict[bcv_schemas.BCVCurrencyEnum, float] | None:
    soup = _get_bcv_soup()
    if not soup:
        return None

    eur_tag = soup.find(id="euro")
    cny_tag = soup.find(id="yuan")
    try_tag = soup.find(id="lira")
    rub_tag = soup.find(id="rublo")
    usd_tag = soup.find(id="dolar")

    if not (eur_tag and cny_tag and try_tag and rub_tag and usd_tag):
        return None

    eur_rate = eur_tag.text.strip()
    cny_rate = cny_tag.text.strip()
    try_rate = try_tag.text.strip()
    rub_rate = rub_tag.text.strip()
    usd_rate = usd_tag.text.strip()

    if not (eur_rate and cny_rate and try_rate and rub_rate and usd_rate):
        return None

    return bcv_schemas.BCVRatesModel.model_validate(
        dict(
            EUR=_parse_bcv_rate(eur_rate),
            CNY=_parse_bcv_rate(cny_rate),
            TRY=_parse_bcv_rate(try_rate),
            RUB=_parse_bcv_rate(rub_rate),
            USD=_parse_bcv_rate(usd_rate),
        )
    ).root
