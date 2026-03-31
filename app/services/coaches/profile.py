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

        # 1. Image URL
        image_url = self.get_text_by_xpath("//div[@id='fotoauswahlOeffnen']/img/@src")
        if image_url and '?' in image_url:
            image_url = image_url.split('?')[0]
        self.response["image_url"] = image_url

        # 2. Citizenship - используем get_text_by_xpath с правильным XPath
        # get_text_by_xpath возвращает строку, если указать правильный путь к тексту
        citizenship = self.get_text_by_xpath("//span[@itemprop='nationality']/text()")
        if citizenship:
            self.response["citizenship"] = trim(citizenship)
        else:
            # Альтернативный вариант: берем текст из всего элемента
            citizenship_elem = self.get_text_by_xpath("//span[@itemprop='nationality']")
            if citizenship_elem:
                # Извлекаем только текст, исключая HTML теги
                import re
                text = re.sub(r'<[^>]+>', '', citizenship_elem)
                self.response["citizenship"] = trim(text)
            else:
                self.response["citizenship"] = None

        # 3. Current club - название и ID
        club_name = self.get_text_by_xpath("//span[@class='data-header__club']/a/text()")
        if club_name:
            club_name = trim(club_name)

        club_url = self.get_text_by_xpath("//span[@class='data-header__club']/a/@href")
        club_id = extract_from_url(club_url) if club_url else None

        self.response["occupation"] = {
            "id": club_id,
            "name": club_name
        }

        return self.response