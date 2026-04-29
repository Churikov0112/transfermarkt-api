from schema import And, Or, Schema

from app.services.national_teams.players import TransfermarktNationalTeamPlayers


def test_get_national_team_players(len_greater_than_0, regex_integer, regex_market_value):
    tfmkt = TransfermarktNationalTeamPlayers(team_id="3299", season_id="2025")
    result = tfmkt.get_national_team_players()

    expected_schema = Schema(
        {
            "id": "3299",
            "seasonId": "2025",
            "players": [
                {
                    "id": And(str, len_greater_than_0, regex_integer),
                    "name": And(str, len_greater_than_0),
                    "position": And(str, len_greater_than_0),
                    "age": And(str, len_greater_than_0, regex_integer),
                    "club": And(str, len_greater_than_0),
                    "marketValue": Or(None, And(str, len_greater_than_0, regex_market_value)),
                },
            ],
        },
    )

    assert expected_schema.validate(result)
