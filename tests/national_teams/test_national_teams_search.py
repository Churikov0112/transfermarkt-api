import pytest
from schema import And, Schema

from app.services.national_teams.search import TransfermarktNationalTeamSearch


def test_search_national_teams_empty(len_equal_to_0):
    tfmkt = TransfermarktNationalTeamSearch(query="zzzzzzzz", page_number=1)
    result = tfmkt.search_national_teams()

    expected_schema = Schema(
        {
            "query": "zzzzzzzz",
            "pageNumber": 1,
            "lastPageNumber": And(int, lambda x: x >= 1),
            "results": And(list, len_equal_to_0),
        },
    )

    assert expected_schema.validate(result)


@pytest.mark.parametrize("query,page_number", [("england", 1), ("france", 1)])
def test_search_national_teams(query, page_number, len_greater_than_0, regex_club_url, regex_market_value, regex_integer):
    tfmkt = TransfermarktNationalTeamSearch(query=query, page_number=page_number)
    result = tfmkt.search_national_teams()

    expected_schema = Schema(
        {
            "query": query,
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
