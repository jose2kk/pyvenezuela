"""BCV Client."""

import collections
import datetime
import re
from typing import Dict, List, Optional

import bs4
import requests

from pyvenezuela.schemas import bcv as bcv_schemas

BCV_URL = "https://www.bcv.org.ve/"
RATES_URL = (
    "https://www.bcv.org.ve/cambiaria/export/tasas-informativas-sistema-bancario"
)


def _request(url: str) -> Optional[str]:
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        # print(response.content.strip())
        return bs4.BeautifulSoup(response.content, "html.parser")
    except requests.HTTPError:
        return None


def _get_bcv_soup() -> Optional[bs4.BeautifulSoup]:
    return _request(url=BCV_URL)


def _get_banks_soup() -> Optional[bs4.BeautifulSoup]:
    return _request(url=RATES_URL)


def _get_rates(
    start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None
) -> Optional[Dict[bcv_schemas.BankEnum, List[bcv_schemas.BCVBankRatesModel]]]:
    if start_date and end_date and start_date > end_date:
        return None

    if not (start_date and end_date):
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=30)

    soup = _get_banks_soup()
    if not soup:
        return None

    data: Dict[str, List[Dict[str, str]]] = collections.defaultdict(list)

    rows: List[bs4.element.Tag] = soup.find_all(name="tr")
    for row in rows:
        columns: List[bs4.element.Tag] = row.find_all(name="td")
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

    return bcv_schemas.BCVBanksRatesModel.model_validate(data)


def _parse_bcv_rate(text: str) -> float:
    return float(re.sub(pattern=r"[^\d,]", repl="", string=text).replace(",", "."))


def get_rates(
    start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None
) -> Optional[Dict[bcv_schemas.BankEnum, List[bcv_schemas.BCVBankRatesModel]]]:
    return _get_rates(start_date=start_date, end_date=end_date)


def get_rates_by_bank(
    bank: bcv_schemas.BankEnum,
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
) -> List[bcv_schemas.BCVBankRatesModel]:
    rates = _get_rates(start_date=start_date, end_date=end_date)

    return rates.get(bank, []) if rates else []


def get_rates_by_bcv() -> Optional[Dict[bcv_schemas.BCVCurrencyEnum, float]]:
    soup = _get_bcv_soup()
    if not soup:
        return None

    print(soup.find(id="block-views-47bbee0af9473fcf0d6df64198f4df6b"))

    eur_rate = soup.find(id="euro").text.strip()
    cny_rate = soup.find(id="yuan").text.strip()
    try_rate = soup.find(id="lira").text.strip()
    rub_rate = soup.find(id="rublo").text.strip()
    usd_rate = soup.find(id="dolar").text.strip()

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
