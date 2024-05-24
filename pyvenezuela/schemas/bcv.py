"""BCV schemas."""

import datetime
import enum
from typing import Dict, List

from pydantic import BaseModel, RootModel, field_validator


class BankEnum(str, enum.Enum):
    """Bank Enum."""

    BANCAMIGA = "Bancamiga"
    BANCARIBE = "BanCaribe"
    BANCO_ACTIVO = "Banco Activo"
    BANCO_BICENTENARIO_DEL_PUEBLO = "Banco Bicentenario del Pueblo"
    BANCO_DE_VENEZUELA = "Banco de Venezuela"
    BANCO_DELSUR = "Delsur"
    BANCO_DEL_TESORO = "Banco del Tesoro"
    BANCO_EXTERIOR = "Banco Exterior"
    BANCO_FONDO_COMUN = "BFC Banco Fondo Común"
    BANCO_NACIONAL_DE_CREDITO = "Banco Nacional de Crédito BNC"
    BANCO_OCCIDENTAL_DE_DESCUENTO = "BOD"
    BANCO_PLAZA = "Banco Plaza"
    BANCO_SOFITASA = "Banco Sofitasa"
    BANCO_VENEZOLANO_DE_CREDITO = "Banco Venezolano de Crédito"
    BANESCO = "Banesco"
    BANPLUS = "Banplus"
    BANCO_MERCANTIL = "Banco Mercantil"
    BBVA_PROVINCIAL = "BBVA Provincial"
    CIEN_PC_BANCO = "100% Banco"
    CITIBANK = "Citibank"
    MI_BANCO = "Mi Banco"
    OTHER_BANKS = "Otras Instituciones"


class BCVBankRatesModel(BaseModel):
    """BCV Bank Rate Model."""

    date: datetime.date
    buy_rate: float
    sell_rate: float

    @field_validator("date", mode="before")
    def validate_date(cls, v: str) -> datetime.date:
        return datetime.datetime.strptime(v, "%d-%m-%Y").date()


class BCVBanksRatesModel(RootModel):
    """BCV Bank Model."""

    root: Dict[BankEnum, List[BCVBankRatesModel]]


class BCVCurrencyEnum(str, enum.Enum):
    """BCV Currencies Enum."""

    EUR = "EUR"
    CNY = "CNY"
    TRY = "TRY"
    RUB = "RUB"
    USD = "USD"


class BCVRatesModel(RootModel):
    """BCV Rates Model."""

    root: Dict[BCVCurrencyEnum, float]
