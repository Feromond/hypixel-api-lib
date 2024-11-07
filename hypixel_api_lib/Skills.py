import requests

SKILLS_API_URL = r"https://api.hypixel.net/v2/resources/skyblock/skills"

class SkillLevel:
    """
    Represents a single level in a skill.
    
    Attributes:
        level (int): The level number.
        total_exp_required (float): The total XP required to reach this level.
        unlocks (list): List of unlocks or rewards for achieving this level.
    """
    
    def __init__(self, level: int, total_exp_required: float, unlocks: list) -> None:
        self.level: int = level
        self.total_exp_required: float = total_exp_required
        self.unlocks: list = unlocks

    def __str__(self) -> str:
        return f"Level {self.level}: Requires {self.total_exp_required} XP, Unlocks: {self.unlocks}"

class Skill:
    """
    Represents a skill with multiple levels.
    
    Attributes:
        name (str): The name of the skill.
        description (str): A brief description of the skill.
        max_level (int): The maximum level a player can reach in this skill.
        levels (list of SkillLevel): A list of SkillLevel objects representing the different levels.
    """
    
    def __init__(self, name: str, description: str, max_level: int, levels_data: list) -> None:
        self.name: str = name
        self.description: str = description
        self.max_level: int = max_level
        self.levels: list[SkillLevel] = [SkillLevel(lvl['level'], lvl['totalExpRequired'], lvl['unlocks']) for lvl in levels_data]

    def get_level(self, level: int) -> SkillLevel | None:
        """
        Retrieve a specific level by its number.
        
        Args:
            level (int): The level to retrieve.

        Returns:
            SkillLevel or None: The SkillLevel object for the requested level, or None if it does not exist.
        """
        return next((lvl for lvl in self.levels if lvl.level == level), None)

    def __str__(self) -> str:
        return f"{self.name} (Max Level: {self.max_level}): {self.description}"

class Skills:
    """
    Handles fetching and managing all the skills from the API.
    
    Attributes:
        api_endpoint (str): The endpoint URL to fetch the skills data.
        skills (dict of str: Skill): A dictionary of skill names (keys) to Skill objects.
    """
    
    def __init__(self, api_endpoint: str = SKILLS_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.skills: dict[str,Skill] | None = None
        self._load_skills()

    def _load_skills(self) -> None:
        """Fetch skills data from the API and initialize Skill objects."""
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()
            
            if "skills" in data and data["skills"]:
                self.skills = {
                    key: Skill(
                        value['name'],
                        value.get('description', ''),
                        value['maxLevel'],
                        value['levels']
                    )
                    for key, value in data["skills"].items()
                }
            else:
                raise ValueError("No skills data available in the response")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def get_skill(self, name: str) -> Skill | str:
        """
        Retrieve a skill by its name.
        
        Args:
            name (str): The name of the skill to retrieve.

        Returns:
            Skill or str: The Skill object, or an error message if the skill is not found.
        """
        return self.skills.get(name.upper(), f"Skill '{name}' not found.")

    def get_skills_by_max_level(self, max_level: int) -> dict[str,Skill]:
        """
        Retrieve all skills that have a specific maximum level.
        
        Args:
            max_level (int): The maximum level to filter skills by.

        Returns:
            dict of str: Skill: A dictionary of skill names to Skill objects where the max level matches.
        """
        return {name: skill for name, skill in self.skills.items() if skill.max_level == max_level}

    def list_skill_names(self) -> list[str]:
        """
        List all available skill names.
        
        Returns:
            list of str: A list of all skill names.
        """
        return [skill.name for skill in self.skills.values()]
