from hypixel_api_lib.utils import convert_timestamp
from datetime import datetime

class Objective:
    """
    Represents a single objective.

    Attributes:
        name (str): The name of the objective.
        status (str): The status of the objective ('COMPLETE', 'IN_PROGRESS', etc.).
        progress (int): Progress made towards the objective.
        completed_at (datetime | None): When the objective was completed.
    """

    def __init__(self, name: str, data: dict) -> None:
        self.name: str = name
        self.status: str = data.get('status', 'IN_PROGRESS')
        self.progress: int = data.get('progress', 0)
        self.completed_at: datetime | None = convert_timestamp(data.get('completed_at'))

    def is_complete(self) -> bool:
        """
        Checks if the objective is complete.

        Returns:
            bool: True if complete, False otherwise.
        """
        return self.status.upper() == 'COMPLETE'

    def __str__(self) -> str:
        return (
            f"Objective(name={self.name}, status={self.status}, progress={self.progress}, "
            f"completed_at={self.completed_at})"
        )
    def __repr__(self) -> str:
        return (
            f"Objective(name={self.name}, status={self.status}, progress={self.progress}, "
            f"completed_at={self.completed_at})"
        )

class Objectives:
    """
    Represents a collection of objectives.

    Attributes:
        objectives (dict[str,Objective]): Dictionary of objectives by name.
    """

    def __init__(self, data: dict) -> None:
        self.objectives: dict[str,Objective] = {}
        self.tutorial_steps: list[str] | None = None
        self._parse_objectives(data)

    def _parse_objectives(self, data: dict) -> None:
        """
        Parses the objectives data and populates the objectives dictionary.

        Args:
            data (dict): The data dictionary.
        """
        for name, obj_data in data.items():
            if name == 'tutorial' and isinstance(obj_data, list):
                self.tutorial_steps = obj_data
            elif isinstance(obj_data, dict):
                self.objectives[name] = Objective(name, obj_data)
            else:
                print(f"Warning: Unexpected data type for objective '{name}': {type(obj_data)}")

    def get_objective(self, name: str) -> Objective | None:
        """
        Retrieves an Objective by name.

        Args:
            name (str): The name of the objective.

        Returns:
            Objective | None: The Objective instance or None if not found.
        """
        return self.objectives.get(name)

    def get_completed_objectives(self) -> dict[str,Objective]:
        """
        Retrieves all completed objectives.

        Returns:
            dict[str,Objective]: Dictionary of completed objectives.
        """
        return {name: obj for name, obj in self.objectives.items() if obj.is_complete()}

    def get_in_progress_objectives(self) -> dict[str,Objective]:
        """
        Retrieves all in-progress objectives.

        Returns:
            dict[str,Objective]: Dictionary of in-progress objectives.
        """
        return {name: obj for name, obj in self.objectives.items() if not obj.is_complete()}

    def __str__(self) -> str:
        objectives_str = '\n'.join(str(obj) for obj in self.objectives.values())
        tutorial_str = f"Tutorial Steps: {self.tutorial_steps}" if self.tutorial_steps else ""
        return f"Objectives:\n{objectives_str}\n{tutorial_str}"
