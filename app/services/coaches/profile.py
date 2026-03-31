from dataclasses import dataclass
from fastapi import HTTPException

from app.services.base import TransfermarktBase


@dataclass
class TransfermarktCoachProfile(TransfermarktBase):
    """
    A simple class to get coach image from Transfermarkt.
    """
    coach_id: str = None
    URL: str = "https://www.transfermarkt.com/-/profil/trainer/{coach_id}"

    def __post_init__(self) -> None:
        """Initialize and fetch the page."""
        self.URL = self.URL.format(coach_id=self.coach_id)
        self.page = self.request_url_page()

    def get_coach_image(self) -> dict:
        """
        Get coach profile image URL.

        Returns:
            dict: A dictionary containing coach id and image_url.
        """
        # Используем XPath с id для поиска изображения
        image_url = self.get_text_by_xpath("//div[@id='fotoauswahlOeffnen']/img/@src")

        if not image_url:
            raise HTTPException(status_code=404, detail="Image not found for this coach")

        # Очищаем URL от параметров (обрезаем ?lm=...)
        if '?' in image_url:
            image_url = image_url.split('?')[0]

        self.response["id"] = self.coach_id
        self.response["image_url"] = image_url

        return self.response