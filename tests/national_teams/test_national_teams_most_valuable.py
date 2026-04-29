import pytest
from schema import And, Schema

from app.services.national_teams.most_valuable import TransfermarktMostValuableNationalTeams


@pytest.mark.parametrize("page_number", [1, 2])
def test_get_most_valuable_national_teams(page_number, len_greater_than_0, regex_club_url, regex_market_value, regex_integer):
    tfmkt = TransfermarktMostValuableNationalTeams(page_number=page_number)
    result = tfmkt.get_most_valuable_national_teams()

    expected_schema = Schema(
        {
            "pageNumber": page_number,
            "lastPageNumber": And(int, lambda x: x >= 1),
            "results": [
                {
                    "id": And(str, len_greater_than_0, regex_integer),
                    "url": And(str, len_greater_than_0, regex_club_url),
                    "name": And(str, len_greater_than_0),
                    "country": And(str, len_greater_than_0),
                    "confederation": And(str, len_greater_than_0),
                    "marketValue": And(str, len_greater_than_0, regex_market_value),
                },
            ],
        },
    )

    assert expected_schema.validate(result)
