from dataclasses import dataclass
from fastapi import HTTPException

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url, trim


@dataclass
class TransfermarktCoachProfile(TransfermarktBase):
    """
    A simple class to get coach data from Transfermarkt.
    """
    coach_id: str = None
    URL: str = "https://www.transfermarkt.com/-/profil/trainer/{coach_id}"

    def __post_init__(self) -> None:
        """Initialize and fetch the page."""
        self.URL = self.URL.format(coach_id=self.coach_id)
        self.page = self.request_url_page()

    def get_coach_profile(self) -> dict:
        """
        Get coach profile information.

        Returns:
            dict: A dictionary containing coach data.
        """
        self.response = {}
        self.response["id"] = self.coach_id

        # 1. Name - собираем все текстовые фрагменты
        name_parts = self.get_list_by_xpath("//h1[@class='data-header__headline-wrapper']//text()")
        if name_parts:
            name = ' '.join([trim(part) for part in name_parts])
            self.response["name"] = name
        else:
            self.response["name"] = None

        # 2. Image URL
        image_url = self.get_text_by_xpath("//div[@id='fotoauswahlOeffnen']/img/@src")
        if image_url and '?' in image_url:
            image_url = image_url.split('?')[0]
        self.response["image_url"] = image_url

        # 3. Citizenship
        citizenship = self.get_text_by_xpath("//span[@itemprop='nationality']/text()")
        if citizenship:
            self.response["citizenship"] = trim(citizenship)
        else:
            self.response["citizenship"] = None

        # 4. Current club
        club_name = self.get_text_by_xpath("//span[@class='data-header__club']/a/text()")
        if club_name:
            club_name = trim(club_name)

        club_url = self.get_text_by_xpath("//span[@class='data-header__club']/a/@href")
        club_id = extract_from_url(club_url) if club_url else None

        self.response["current_club"] = {
            "id": club_id,
            "name": club_name
        }

        return self.response