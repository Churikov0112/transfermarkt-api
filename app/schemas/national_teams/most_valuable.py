from typing import Optional

from app.schemas.base import AuditMixin, TransfermarktBaseModel


class MostValuableNationalTeamResult(TransfermarktBaseModel):
    id: str
    url: str
    name: str
    country: str
    confederation: str
    market_value: Optional[int] = None


class MostValuableNationalTeams(TransfermarktBaseModel, AuditMixin):
    page_number: int
    last_page_number: int
    results: list[MostValuableNationalTeamResult]
