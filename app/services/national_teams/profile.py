from dataclasses import dataclass

from app.services.clubs.profile import TransfermarktClubProfile


@dataclass
class TransfermarktNationalTeamProfile(TransfermarktClubProfile):
    """
    A class for retrieving and parsing national team profile information.

    Args:
        team_id (str): The unique identifier of the national team.
    """

    team_id: str = None

    def __post_init__(self) -> None:
        self.club_id = self.team_id
        super().__post_init__()

    def get_national_team_profile(self) -> dict:
        """Retrieve and parse the profile information of the national team."""
        return self.get_club_profile()
