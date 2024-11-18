from datetime import datetime
import requests
from hypixel_api_lib.utils import convert_timestamp

ELECTIONS_API_URL = r"https://api.hypixel.net/v2/resources/skyblock/election"

class Perk:
    """
    Represents a mayoral perk.

    Attributes:
        name (str): The name of the perk.
        description (str): The description of the perk.
        minister (bool | None): Indicates if the candidate will be the Minister for this perk if elected.
    """
    def __init__(self, perk_data: dict) -> None:
        self.name: str = perk_data.get('name', 'Unknown Perk')
        self.description: str = perk_data.get('description', '')
        self.minister: bool | None = perk_data.get('minister')

    def __str__(self) -> str:
        minister_str = f" (Minister: {self.minister})" if self.minister is not None else ""
        return f"{self.name}: {self.description}{minister_str}"
    
    def __repr__(self) -> str:
        minister_str = f" (Minister: {self.minister})" if self.minister is not None else ""
        return f"{self.name}: {self.description}{minister_str}"

class Candidate:
    """
    Represents a candidate in an election.

    Attributes:
        key (str): The candidate's unique key.
        name (str): The candidate's name.
        perks (list of Perk): The perks offered by the candidate.
        votes (int): The number of votes the candidate has received.
    """
    def __init__(self, candidate_data: dict) -> None:
        self.key: str = candidate_data.get('key')
        self.name: str = candidate_data.get('name', 'Unknown Candidate')
        self.perks: list[Perk] = [Perk(perk) for perk in candidate_data.get('perks', [])]
        self.votes: int = candidate_data.get('votes', 0)

    def __str__(self) -> str:
        return f"Candidate {self.name} (Key: {self.key}): {self.votes} votes"

class Election:
    """
    Represents an election.

    Attributes:
        year (int): The year of the election.
        candidates (list of Candidate): The list of candidates in the election.
    """
    def __init__(self, election_data: dict) -> None:
        self.year: int = election_data.get('year', 0)
        self.candidates: list[Candidate] = [Candidate(candidate) for candidate in election_data.get('candidates', [])]

    def get_candidate_by_key(self, key: str) -> Candidate | None:
        """
        Retrieve a candidate by their key.

        Args:
            key (str): The key of the candidate.

        Returns:
            Candidate or None: The Candidate object, or None if not found.
        """
        return next((candidate for candidate in self.candidates if candidate.key == key), None)

    def get_candidate_by_name(self, name: str) -> Candidate | None:
        """
        Retrieve a candidate by their name.

        Args:
            name (str): The name of the candidate.

        Returns:
            Candidate or None: The Candidate object, or None if not found.
        """
        return next((candidate for candidate in self.candidates if candidate.name.lower() == name.lower()), None)

    def get_ministers(self, mayor_key: str) -> list[tuple[Candidate, list[Perk]]]:
        """
        Retrieves the ministers from this election.

        Args:
            mayor_key (str): The key of the elected mayor.

        Returns:
            list of tuples: Each tuple contains a Candidate object and a list of their Perks where 'minister' is True.
        """
        ministers = []
        for candidate in self.candidates:
            if candidate.key != mayor_key:
                minister_perks = [perk for perk in candidate.perks if perk.minister]
                if minister_perks:
                    ministers.append((candidate, minister_perks))
        return ministers

    def __str__(self) -> str:
        return f"Election Year {self.year} with {len(self.candidates)} candidates"

class Mayor:
    """
    Represents the current mayor.

    Attributes:
        key (str): The mayor's unique key.
        name (str): The mayor's name.
        perks (list of Perk): The list of perks offered by the mayor.
        election (Election): The election in which the mayor was elected.
    """
    def __init__(self, mayor_data: dict) -> None:
        self.key: str = mayor_data.get('key')
        self.name: str = mayor_data.get('name', 'Unknown Mayor')
        self.perks: list[Perk] = [Perk(perk) for perk in mayor_data.get('perks', [])]
        self.election: Election | None = None
        if 'election' in mayor_data:
            self.election = Election(mayor_data['election'])
    
    def get_ministers(self) -> list[tuple[Candidate, list[Perk]]]:
        """
        Retrieves the ministers from the mayor's election.

        Returns:
            list of tuples: Each tuple contains a Candidate object and a list of their Perks where 'minister' is True.
        """
        if self.election:
            return self.election.get_ministers(self.key)
        return []

    def __str__(self) -> str:
        return f"Mayor {self.name} (Key: {self.key})"

class Elections:
    """
    Manages fetching and storing the elections data from the API.

    Attributes:
        last_updated (datetime): The timestamp of the last update.
        mayor (Mayor): The current mayor.
        current_election (Election): The current election.
    """
    def __init__(self, api_endpoint: str = ELECTIONS_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.last_updated: datetime | None = None
        self.mayor: Mayor | None = None
        self.current_election: Election | None = None
        self._load_elections_data()

    def _load_elections_data(self) -> None:
        """Fetch the elections data from the API."""
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                self.last_updated = convert_timestamp(data.get('lastUpdated'))
                self.mayor = Mayor(data.get('mayor', {}))
                self.current_election = Election(data.get('current', {}))
            else:
                raise ValueError("Failed to fetch elections data")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def get_current_election(self) -> Election | None:
        """
        Get the current election.

        Returns:
            Election or None: The current election.
        """
        return self.current_election

    def get_mayor(self) -> Mayor | None:
        """
        Get the current mayor.

        Returns:
            Mayor or None: The current mayor.
        """
        return self.mayor

    def __str__(self) -> str:
        mayor_str = str(self.mayor) if self.mayor else "No current mayor"
        election_str = str(self.current_election) if self.current_election else "No current election"
        return f"{mayor_str}\n{election_str}"
