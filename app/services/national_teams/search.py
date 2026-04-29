from dataclasses import dataclass

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url
from app.utils.xpath import NationalTeams


@dataclass
class TransfermarktNationalTeamSearch(TransfermarktBase):
    """
    A class for searching national teams in the Transfermarkt ranking page.

    Args:
        query (str): National team search text.
        page_number (int): Ranking page number.
        URL (str): URL template for the ranking page.
    """

    query: str = None
    page_number: int = 1
    URL: str = "https://www.transfermarkt.com/vereins-statistik/wertvollstenationalmannschaften/marktwertetop?page={page_number}"

    def __post_init__(self) -> None:
        """Initialize the TransfermarktNationalTeamSearch class."""
        self.URL = self.URL.format(page_number=self.page_number)
        self.page = self.request_url_page()

    def __parse_search_results(self) -> list:
        """
        Parse ranking rows and filter them by query.

        Returns:
            list: Filtered national teams with ranking metadata.
        """
        urls = self.get_list_by_xpath(NationalTeams.MostValuable.URLS)
        names = self.get_list_by_xpath(NationalTeams.MostValuable.NAMES)
        countries = self.get_list_by_xpath(NationalTeams.MostValuable.COUNTRIES)
        confederations = self.get_list_by_xpath(NationalTeams.MostValuable.CONFEDERATIONS)
        market_values = self.get_list_by_xpath(NationalTeams.MostValuable.MARKET_VALUES)
        ids = [extract_from_url(url) for url in urls]
        query_normalized = (self.query or "").lower()

        results = []
        for idx, url, name, country, confederation, market_value in zip(
            ids,
            urls,
            names,
            countries,
            confederations,
            market_values,
        ):
            if query_normalized not in name.lower() and query_normalized not in country.lower():
                continue
            results.append(
                {
                    "id": idx,
                    "url": url,
                    "name": name,
                    "country": country,
                    "confederation": confederation,
                    "marketValue": market_value,
                }
            )

        return results

    def search_national_teams(self) -> dict:
        """
        Search national teams by name from ranking page.

        Returns:
            dict: Query metadata, pagination metadata and filtered rows.
        """
        self.response["query"] = self.query
        self.response["pageNumber"] = self.page_number
        self.response["lastPageNumber"] = self.get_last_page_number()
        self.response["results"] = self.__parse_search_results()

        return self.response
