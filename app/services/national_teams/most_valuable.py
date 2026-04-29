from dataclasses import dataclass

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url
from app.utils.xpath import NationalTeams


@dataclass
class TransfermarktMostValuableNationalTeams(TransfermarktBase):
    """
    A class for scraping most valuable national teams from Transfermarkt.

    Args:
        page_number (int): Ranking page number.
        URL (str): URL template for the ranking page.
    """

    page_number: int = 1
    URL: str = "https://www.transfermarkt.com/vereins-statistik/wertvollstenationalmannschaften/marktwertetop?page={page_number}"

    def __post_init__(self) -> None:
        """Initialize the TransfermarktMostValuableNationalTeams class."""
        self.URL = self.URL.format(page_number=self.page_number)
        self.page = self.request_url_page()

    def __parse_results(self) -> list:
        """
        Parse the ranking table and extract data about national teams.

        Returns:
            list: Parsed ranking rows with id, url, name, country, confederation and market value.
        """
        urls = self.get_list_by_xpath(NationalTeams.MostValuable.URLS)
        names = self.get_list_by_xpath(NationalTeams.MostValuable.NAMES)
        countries = self.get_list_by_xpath(NationalTeams.MostValuable.COUNTRIES)
        confederations = self.get_list_by_xpath(NationalTeams.MostValuable.CONFEDERATIONS)
        market_values = self.get_list_by_xpath(NationalTeams.MostValuable.MARKET_VALUES)
        ids = [extract_from_url(url) for url in urls]

        return [
            {
                "id": idx,
                "url": url,
                "name": name,
                "country": country,
                "confederation": confederation,
                "marketValue": market_value,
            }
            for idx, url, name, country, confederation, market_value in zip(
                ids,
                urls,
                names,
                countries,
                confederations,
                market_values,
            )
        ]

    def get_most_valuable_national_teams(self) -> dict:
        """
        Retrieve most valuable national teams for a ranking page.

        Returns:
            dict: Current page number, last page number, parsed rows and audit timestamp.
        """
        self.response["pageNumber"] = self.page_number
        self.response["lastPageNumber"] = self.get_last_page_number()
        self.response["results"] = self.__parse_results()

        return self.response
