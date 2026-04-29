import pytest
from fastapi import HTTPException
from schema import And, Schema

from app.services.national_teams.profile import TransfermarktNationalTeamProfile


def test_get_national_team_profile_not_found():
    with pytest.raises(HTTPException):
        TransfermarktNationalTeamProfile(team_id="0")


@pytest.mark.parametrize("team_id", ["3299", "3377"])
def test_get_national_team_profile(team_id, len_greater_than_0, regex_club_url):
    tfmkt = TransfermarktNationalTeamProfile(team_id=team_id)
    result = tfmkt.get_national_team_profile()

    expected_schema = Schema(
        {
            "id": team_id,
            "url": And(str, len_greater_than_0, regex_club_url),
            "name": And(str, len_greater_than_0),
        },
        ignore_extra_keys=True,
    )

    assert expected_schema.validate(result)
