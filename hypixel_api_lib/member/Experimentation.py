from datetime import datetime
from hypixel_api_lib.utils import convert_timestamp

class Experiment:
    """
    Represents a generic Experiment.

    Attributes:
        last_attempt (datetime): The time of the last attempt.
        last_claimed (datetime): The time the last reward was claimed.
        attempts (dict[int,int]): Number of attempts per level.
        claims (dict[int,int]): Number of claims per level.
        best_scores (dict[int,int]): Best scores per level.
    """

    def __init__(self, data: dict) -> None:
        self.last_attempt: datetime | None = convert_timestamp(data.get('last_attempt'))
        self.last_claimed: datetime | None = convert_timestamp(data.get('last_claimed'))
        self.attempts: dict[int,int] = {}
        self.claims: dict[int,int] = {}
        self.best_scores: dict[int,int] = {}

        for key, value in data.items():
            if key.startswith('attempts_'):
                level = int(key.split('_')[-1])
                self.attempts[level] = value
            elif key.startswith('claims_'):
                level = int(key.split('_')[-1])
                self.claims[level] = value
            elif key.startswith('best_score_'):
                level = int(key.split('_')[-1])
                self.best_scores[level] = value

    def __str__(self) -> str:
        return (
            f"Experiment - Last Attempt: {self.last_attempt}, Last Claimed: {self.last_claimed}, "
            f"Attempts: {self.attempts}, Claims: {self.claims}, Best Scores: {self.best_scores}"
        )

class BonusClicksExperiment(Experiment):
    """
    Represents an Experiment that includes bonus clicks (e.g., Simon and Numbers).

    Attributes:
        bonus_clicks (int): Number of bonus clicks available.
    """

    def __init__(self, data: dict):
        super().__init__(data)
        self.bonus_clicks: int = data.get('bonus_clicks', 0)

    def __str__(self):
        return (
            f"BonusClicksExperiment - Last Attempt: {self.last_attempt}, Last Claimed: {self.last_claimed}, "
            f"Bonus Clicks: {self.bonus_clicks}, Attempts: {self.attempts}, "
            f"Claims: {self.claims}, Best Scores: {self.best_scores}"
        )

class Experimentation:
    """
    Represents the experimentation data.

    Attributes:
        pairings (Experiment): Pairings experiment data.
        simon (BonusClicksExperiment): Simon experiment data.
        numbers (BonusClicksExperiment): Numbers experiment data.
        claims_resets (int): Number of claim resets.
        claims_resets_timestamp (datetime): Timestamp of the last claim reset.
        serums_drank (int): Number of serums consumed.
    """

    def __init__(self, data: dict) -> None:
        self.pairings: Experiment = Experiment(data.get('pairings', {}))
        self.simon: BonusClicksExperiment = BonusClicksExperiment(data.get('simon', {}))
        self.numbers: BonusClicksExperiment = BonusClicksExperiment(data.get('numbers', {}))
        self.claims_resets: int = data.get('claims_resets', 0)
        self.claims_resets_timestamp: datetime | None = convert_timestamp(data.get('claims_resets_timestamp'))
        self.serums_drank: int = data.get('serums_drank', 0)

    def __str__(self) -> str:
        return (
            f"Experimentation Data - Serums Drank: {self.serums_drank}, "
            f"Claims Resets: {self.claims_resets}, Claims Resets Timestamp: {self.claims_resets_timestamp}"
        )
