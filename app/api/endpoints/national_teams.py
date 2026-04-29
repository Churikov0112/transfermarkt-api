from typing import Optional

from fastapi import APIRouter

from app.schemas import national_teams as schemas
from app.services.national_teams.most_valuable import TransfermarktMostValuableNationalTeams
from app.services.national_teams.search import TransfermarktNationalTeamSearch

router = APIRouter()


@router.get("/most-valuable", response_model=schemas.MostValuableNationalTeams, response_model_exclude_none=True)
def get_most_valuable_national_teams(page_number: Optional[int] = 1) -> dict:
    tfmkt = TransfermarktMostValuableNationalTeams(page_number=page_number)
    national_teams = tfmkt.get_most_valuable_national_teams()
    return national_teams


@router.get("/search/{team_name}", response_model=schemas.NationalTeamSearch, response_model_exclude_none=True)
def search_national_teams(team_name: str, page_number: Optional[int] = 1) -> dict:
    tfmkt = TransfermarktNationalTeamSearch(query=team_name, page_number=page_number)
    national_teams = tfmkt.search_national_teams()
    return national_teams
