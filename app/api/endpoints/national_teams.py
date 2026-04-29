from typing import Optional

from fastapi import APIRouter

from app.schemas import national_teams as schemas
from app.services.national_teams.most_valuable import TransfermarktMostValuableNationalTeams
from app.services.national_teams.players import TransfermarktNationalTeamPlayers
from app.services.national_teams.profile import TransfermarktNationalTeamProfile
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


@router.get("/{team_id}/profile", response_model=schemas.NationalTeamProfile, response_model_exclude_defaults=True)
def get_national_team_profile(team_id: str) -> dict:
    tfmkt = TransfermarktNationalTeamProfile(team_id=team_id)
    national_team_profile = tfmkt.get_national_team_profile()
    return national_team_profile


@router.get("/{team_id}/players", response_model=schemas.NationalTeamPlayers, response_model_exclude_defaults=True)
def get_national_team_players(team_id: str, season_id: Optional[str] = None) -> dict:
    tfmkt = TransfermarktNationalTeamPlayers(team_id=team_id, season_id=season_id)
    national_team_players = tfmkt.get_national_team_players()
    return national_team_players
